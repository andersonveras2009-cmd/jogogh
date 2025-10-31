# jogos_3em1_final.py
# 3-em-1: Dama (Checkers), Xadrez (simplified), Ludo (simplified)
# Funciona no Pydroid 3 e PC com pygame. IA simples (movimentos aleatórios válidos).
# Salve como jogos_3em1_final.py e execute (requer pygame).

import pygame, sys, random, math, traceback
pygame.init()
pygame.font.init()

# --- Janela / constantes ---
W, H = 900, 700
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("3 em 1 - Dama / Xadrez / Ludo")
FPS = 30
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 20)
BIG = pygame.font.SysFont(None, 30)

# cores
WHITE = (255,255,255); BLACK = (0,0,0); GRAY=(200,200,200)
DARK = (181,136,99); LIGHT=(240,217,181)
RED = (200,30,30); GREEN=(34,177,76); BLUE=(0,102,204); YELLOW=(255,230,0)

def text(surf, t, x, y, col=BLACK, font=FONT):
    surf.blit(font.render(str(t), True, col), (x,y))

def center_text(surf, t, x, y, col=BLACK, font=BIG):
    r = font.render(str(t), True, col)
    rect = r.get_rect(center=(x,y))
    surf.blit(r, rect)

class Button:
    def __init__(self, rect, label, cb=None):
        self.rect = pygame.Rect(rect); self.label = label; self.cb = cb
    def draw(self, surf):
        pygame.draw.rect(surf, GRAY, self.rect, border_radius=6)
        pygame.draw.rect(surf, BLACK, self.rect, 2, border_radius=6)
        center_text(surf, self.label, self.rect.centerx, self.rect.centery, col=BLACK, font=FONT)
    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    def click(self):
        if self.cb: return self.cb()

# ------------------ Menu ------------------
def main_menu():
    b_dama = Button((320,180,260,50),"Dama", lambda: dama_menu())
    b_xad = Button((320,250,260,50),"Xadrez", lambda: xadrez_menu())
    b_ludo = Button((320,320,260,50),"Ludo", lambda: ludo_menu())
    b_quit = Button((320,390,260,50),"Sair", lambda: sys.exit(0))
    buttons = [b_dama,b_xad,b_ludo,b_quit]
    while True:
        SCREEN.fill(WHITE)
        center_text(SCREEN, "3 em 1 - Dama / Xadrez / Ludo", W//2, 100)
        for b in buttons: b.draw(SCREEN)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                pos = ev.pos
                for b in buttons:
                    if b.clicked(pos):
                        b.click()
        CLOCK.tick(FPS)

# ------------------ Dama (Checkers) ------------------
def dama_menu():
    b_vs = Button((300,200,300,50),"Jogar vs CPU", lambda: run_checkers(vs_cpu=True))
    b_1v1 = Button((300,270,300,50),"1x1 (amigos)", lambda: run_checkers(vs_cpu=False))
    b_back = Button((300,340,300,50),"Voltar", lambda: 'back')
    while True:
        SCREEN.fill(WHITE)
        center_text(SCREEN, "Dama - Escolha modo", W//2, 120)
        for b in (b_vs,b_1v1,b_back): b.draw(SCREEN)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                if b_vs.clicked(ev.pos): b_vs.click()
                if b_1v1.clicked(ev.pos): b_1v1.click()
                if b_back.clicked(ev.pos): return
        CLOCK.tick(FPS)

def run_checkers(vs_cpu=False):
    try:
        S = 8
        tile = min( (W-120)//S, (H-160)//S )
        ox, oy = 40, 40
        # board: None or dict {'color':'white'/'black','king':bool}
        board = [[None]*S for _ in range(S)]
        for r in range(3):
            for c in range(S):
                if (r+c)%2==1:
                    board[r][c] = {'color':'black','king':False}
        for r in range(S-3,S):
            for c in range(S):
                if (r+c)%2==1:
                    board[r][c] = {'color':'white','king':False}
        turn = 'white'
        selected = None
        winner = None
        def inb(r,c): return 0<=r<S and 0<=c<S
        def gen_moves(r,c):
            p = board[r][c]
            if not p: return []
            dirs=[(-1,-1),(-1,1),(1,-1),(1,1)]
            jumps=[]; moves=[]
            for dr,dc in dirs:
                nr,nc = r+dr,c+dc
                if not inb(nr,nc): continue
                if board[nr][nc] is None:
                    if p['king'] or (p['color']=='white' and dr==-1) or (p['color']=='black' and dr==1):
                        moves.append((nr,nc))
                else:
                    jr,jc = nr+dr, nc+dc
                    if inb(jr,jc) and board[jr][jc] is None and board[nr][nc]['color']!=p['color']:
                        jumps.append((jr,jc,nr,nc))
            return jumps if jumps else moves
        def has_moves(color):
            for r in range(S):
                for c in range(S):
                    p = board[r][c]
                    if p and p['color']==color and gen_moves(r,c):
                        return True
            return False
        def apply_move(fr,fc,tr,tc):
            nonlocal board
            p = board[fr][fc]
            board[tr][tc] = p
            board[fr][fc] = None
            if abs(tr-fr)==2:
                mr,mc = (fr+tr)//2, (fc+tc)//2
                board[mr][mc] = None
            if p and not p['king']:
                if p['color']=='white' and tr==0: p['king']=True
                if p['color']=='black' and tr==S-1: p['king']=True
        def cpu_play():
            nonlocal turn
            moves=[]; jumps=[]
            for r in range(S):
                for c in range(S):
                    p = board[r][c]
                    if p and p['color']==turn:
                        g = gen_moves(r,c)
                        if g:
                            if isinstance(g[0], tuple) and len(g[0])==4:
                                for t in g: jumps.append((r,c,t[0],t[1]))
                            else:
                                for t in g: moves.append((r,c,t[0],t[1]))
            if jumps:
                fr,fc,tr,tc = random.choice(jumps)
            elif moves:
                fr,fc,tr,tc = random.choice(moves)
            else:
                return
            apply_move(fr,fc,tr,tc)
            # chain jumps
            if abs(tr-fr)==2:
                chain = gen_moves(tr,tc)
                while chain and isinstance(chain[0], tuple) and len(chain[0])==4:
                    ch = random.choice(chain)
                    apply_move(tr,tc,ch[0],ch[1])
                    tr,tc = ch[0],ch[1]
                    chain = gen_moves(tr,tc)
            turn = 'white' if turn=='black' else 'black'
        # loop
        while True:
            SCREEN.fill(WHITE)
            # draw board
            for r in range(S):
                for c in range(S):
                    x,y = ox+c*tile, oy+r*tile
                    col = LIGHT if (r+c)%2==0 else DARK
                    pygame.draw.rect(SCREEN, col, (x,y,tile,tile))
                    p = board[r][c]
                    if p:
                        cx,cy = x+tile//2, y+tile//2
                        colp = BLACK if p['color']=='black' else WHITE
                        pygame.draw.circle(SCREEN, colp, (cx,cy), tile//2-8)
                        if p['king']:
                            text(SCREEN, "K", cx-6, cy-10, RED)
            center_text(SCREEN, f"Dama - Turno: {turn}  (ESC volta)", W//2, 16)
            pygame.display.flip()
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit(); sys.exit(0)
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE:
                    return
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    mx,my = ev.pos
                    if ox<=mx<ox+S*tile and oy<=my<oy+S*tile:
                        c = (mx-ox)//tile; r = (my-oy)//tile
                        if selected is None:
                            if board[r][c] and board[r][c]['color']==turn:
                                selected = (r,c)
                        else:
                            fr,fc = selected
                            g = gen_moves(fr,fc)
                            legal=False
                            if g:
                                if isinstance(g[0], tuple) and len(g[0])==4:
                                    for t in g:
                                        if (r,c)==(t[0],t[1]): legal=True; break
                                else:
                                    for t in g:
                                        if (r,c)==t: legal=True; break
                            if legal:
                                apply_move(fr,fc,r,c)
                                # chain jumps automatic for simplicity:
                                if abs(r-fr)==2:
                                    cr,cc = r,c
                                    chain = gen_moves(cr,cc)
                                    while chain and isinstance(chain[0], tuple) and len(chain[0])==4:
                                        ch = random.choice(chain)
                                        apply_move(cr,cc,ch[0],ch[1])
                                        cr,cc = ch[0],ch[1]
                                        chain = gen_moves(cr,cc)
                                turn = 'white' if turn=='black' else 'black'
                            selected = None
            # win check
            if not has_moves('white'):
                center_text(SCREEN, "Vencedor: black  (ESC para menu)", W//2, H-30, RED)
            if not has_moves('black'):
                center_text(SCREEN, "Vencedor: white  (ESC para menu)", W//2, H-30, RED)
            pygame.display.flip()
            if vs_cpu and turn=='black':
                pygame.time.delay(300)
                cpu_play()
            CLOCK.tick(FPS)
    except Exception:
        show_exception(traceback.format_exc())
        return

# ------------------ Xadrez (simplified) ------------------
def xadrez_menu():
    b_vs = Button((300,200,300,50),"Jogar vs CPU", lambda: run_chess(vs_cpu=True))
    b_1v1 = Button((300,270,300,50),"1x1 (amigos)", lambda: run_chess(vs_cpu=False))
    b_back = Button((300,340,300,50),"Voltar", lambda: 'back')
    while True:
        SCREEN.fill(WHITE)
        center_text(SCREEN, "Xadrez - Escolha modo", W//2, 120)
        for b in (b_vs,b_1v1,b_back): b.draw(SCREEN)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                if b_vs.clicked(ev.pos): b_vs.click()
                if b_1v1.clicked(ev.pos): b_1v1.click()
                if b_back.clicked(ev.pos): return
        CLOCK.tick(FPS)

def run_chess(vs_cpu=False):
    try:
        S=8
        tile = min( (W-120)//S, (H-160)//S )
        ox, oy = 40, 40
        # board: None or {'type':char, 'color':'white'/'black'}
        board = [[None]*S for _ in range(S)]
        order = ['R','N','B','Q','K','B','N','R']
        for c,ch in enumerate(order):
            board[0][c] = {'type':ch,'color':'black'}
            board[1][c] = {'type':'P','color':'black'}
            board[6][c] = {'type':'P','color':'white'}
            board[7][c] = {'type':order[c],'color':'white'}
        turn = 'white'
        selected = None
        def inb(r,c): return 0<=r<S and 0<=c<S
        def gen_moves(r,c):
            p = board[r][c]; moves=[]
            if not p: return moves
            t = p['type']; col = p['color']
            if t=='P':
                dr = -1 if col=='white' else 1
                if inb(r+dr,c) and board[r+dr][c] is None:
                    moves.append((r+dr,c))
                    start = 6 if col=='white' else 1
                    if r==start and inb(r+2*dr,c) and board[r+2*dr][c] is None: moves.append((r+2*dr,c))
                for dc in (-1,1):
                    nr,nc = r+dr, c+dc
                    if inb(nr,nc) and board[nr][nc] and board[nr][nc]['color']!=col: moves.append((nr,nc))
            if t in ('R','Q','B'):
                dirs=[]
                if t in ('R','Q'): dirs += [(-1,0),(1,0),(0,-1),(0,1)]
                if t in ('B','Q'): dirs += [(-1,-1),(-1,1),(1,-1),(1,1)]
                for dr,dc in dirs:
                    nr,nc = r+dr,c+dc
                    while inb(nr,nc):
                        if board[nr][nc] is None:
                            moves.append((nr,nc))
                        else:
                            if board[nr][nc]['color']!=col: moves.append((nr,nc))
                            break
                        nr+=dr; nc+=dc
            if t=='N':
                for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                    nr,nc = r+dr,c+dc
                    if inb(nr,nc) and (board[nr][nc] is None or board[nr][nc]['color']!=col): moves.append((nr,nc))
            if t=='K':
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if dr==0 and dc==0: continue
                        nr,nc = r+dr,c+dc
                        if inb(nr,nc) and (board[nr][nc] is None or board[nr][nc]['color']!=col): moves.append((nr,nc))
            return moves
        def apply_move(fr,fc,tr,tc):
            p = board[fr][fc]; board[tr][tc] = p; board[fr][fc] = None
            if p and p['type']=='P':
                if p['color']=='white' and tr==0: p['type']='Q'
                if p['color']=='black' and tr==7: p['type']='Q'
        def cpu_play():
            nonlocal turn
            allm=[]
            for r in range(S):
                for c in range(S):
                    p = board[r][c]
                    if p and p['color']==turn:
                        for mv in gen_moves(r,c): allm.append((r,c,mv[0],mv[1]))
            if not allm: return
            fr,fc,tr,tc = random.choice(allm)
            apply_move(fr,fc,tr,tc)
            turn = 'white' if turn=='black' else 'black'
        while True:
            SCREEN.fill(WHITE)
            for r in range(S):
                for c in range(S):
                    x,y = ox + c*tile, oy + r*tile
                    col = LIGHT if (r+c)%2==0 else DARK
                    pygame.draw.rect(SCREEN, col, (x,y,tile,tile))
                    p = board[r][c]
                    if p:
                        cx,cy = x+tile//2, y+tile//2
                        pygame.draw.circle(SCREEN, BLACK if p['color']=='black' else WHITE, (cx,cy), tile//2-10)
                        text(SCREEN, p['type'], cx-8, cy-12, RED)
            center_text(SCREEN, f"Xadrez - Turno: {turn}  (ESC volta)", W//2, 16)
            pygame.display.flip()
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: return
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    mx,my = ev.pos
                    if ox<=mx<ox+S*tile and oy<=my<oy+S*tile:
                        c = (mx-ox)//tile; r = (my-oy)//tile
                        if selected is None:
                            if board[r][c] and board[r][c]['color']==turn:
                                selected = (r,c)
                        else:
                            fr,fc = selected
                            mvs = gen_moves(fr,fc)
                            if (r,c) in mvs:
                                apply_move(fr,fc,r,c)
                                turn = 'white' if turn=='black' else 'black'
                            selected = None
            if vs_cpu and turn=='black':
                pygame.time.delay(200)
                cpu_play()
            CLOCK.tick(FPS)
    except Exception:
        show_exception(traceback.format_exc())
        return

# ------------------ Ludo (simplified) ------------------
def ludo_menu():
    # choose number players and vs cpu toggle
    players = 2; vs_cpu=False
    while True:
        SCREEN.fill(WHITE)
        center_text(SCREEN, "Ludo - Configuração", W//2, 80)
        text(SCREEN, f"Nº jogadores: {players}", 120, 160)
        text(SCREEN, f"Vs CPU (último): {'Sim' if vs_cpu else 'Não'}", 120, 200)
        pygame.draw.rect(SCREEN, GRAY, (120,260,120,40)); text(SCREEN, "-", 170, 268, BLACK, FONT)
        pygame.draw.rect(SCREEN, GRAY, (260,260,120,40)); text(SCREEN, "+", 310, 268, BLACK, FONT)
        pygame.draw.rect(SCREEN, GRAY, (120,320,120,40)); text(SCREEN, "Toggle CPU", 130, 328, BLACK, FONT)
        pygame.draw.rect(SCREEN, GRAY, (260,320,120,40)); text(SCREEN, "Iniciar", 300, 328, BLACK, FONT)
        pygame.draw.rect(SCREEN, GRAY, (120,380,260,40)); text(SCREEN, "Voltar", 240, 388, BLACK, FONT)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                x,y = ev.pos
                if 120<=x<=240 and 260<=y<=300: players = max(2, players-1)
                elif 260<=x<=380 and 260<=y<=300: players = min(4, players+1)
                elif 120<=x<=240 and 320<=y<=360: vs_cpu = not vs_cpu
                elif 260<=x<=380 and 320<=y<=360: run_ludo(players, vs_cpu)
                elif 120<=x<=380 and 380<=y<=420: return
        CLOCK.tick(FPS)

def run_ludo(num_players=2, vs_cpu=False):
    try:
        center = (W//2, H//2)
        radius = 240
        # ring positions
        ring=[]
        for i in range(52):
            ang = 2*math.pi * i / 52
            ring.append((int(center[0]+radius*math.cos(ang)), int(center[1]+radius*math.sin(ang))))
        colors = [RED, GREEN, YELLOW, BLUE]
        players=[]
        for i in range(num_players):
            players.append({'color':colors[i],'tokens':[-1,-1,-1,-1],'start':i*13})
        # final paths: simple inward positions
        final_paths = {}
        for i,p in enumerate(players):
            s = p['start']; path=[]
            for step in range(6):
                idx = (s + step) % 52
                bx,by = ring[idx]; fx = (bx+center[0])//2; fy=(by+center[1])//2
                path.append((fx,fy))
            final_paths[p['color']] = path
        turn = 0; dice = 0; wait_roll=True; message="Clique para rolar"
        ai_flags = [False]*num_players
        if vs_cpu: ai_flags[-1]=True
        def roll(): return random.randint(1,6)
        def legal_moves(pi, dv):
            p = players[pi]; moves=[]
            for ti,pos in enumerate(p['tokens']):
                if pos==-1:
                    if dv==6: moves.append((ti, p['start']))
                elif 0<=pos<52:
                    new = (pos + dv) % 52
                    # enter final simplified: if passes start -> go to final path
                    dist = (p['start'] - pos) % 52
                    if dv > dist:
                        step_into = dv - dist - 1
                        if step_into < 6: moves.append((ti, 100 + step_into + (pi*6)))
                    else:
                        moves.append((ti, new))
                else:
                    idx = pos - 100
                    nid = idx + dv
                    if nid < 6: moves.append((ti, 100 + nid))
            return moves
        def apply_move(pi, ti, newpos):
            p = players[pi]; p['tokens'][ti] = newpos
            # capture on ring
            if 0<=newpos<52:
                for oj,op in enumerate(players):
                    if oj==pi: continue
                    for ot,val in enumerate(op['tokens']):
                        if val==newpos: op['tokens'][ot] = -1
        # loop
        while True:
            SCREEN.fill(WHITE)
            text(SCREEN, f"Ludo - Jogador {turn+1} ({'CPU' if ai_flags[turn] else 'Hum'}) - {message}", 10, 10, BLACK, FONT)
            # draw ring
            for (x,y) in ring: pygame.draw.circle(SCREEN, GRAY, (x,y), 10)
            # draw finals
            for col,path in final_paths.items():
                for (x,y) in path: pygame.draw.circle(SCREEN, (230,230,230), (x,y), 10)
            # draw tokens and bases
            for i,p in enumerate(players):
                base_x = 60 + i*200; base_y = H - 120
                text(SCREEN, f"Jog {i+1}", base_x, base_y-30, BLACK)
                for ti,pos in enumerate(p['tokens']):
                    if pos==-1:
                        tx,ty = base_x + ti*30, base_y
                        pygame.draw.circle(SCREEN, p['color'], (tx,ty), 14)
                        text(SCREEN, str(ti+1), tx-6, ty-8, WHITE)
                    elif 0<=pos<52:
                        bx,by = ring[pos]; pygame.draw.circle(SCREEN, p['color'], (bx,by), 14); text(SCREEN, str(ti+1), bx-6, by-8, WHITE)
                    else:
                        idx = pos-100; fx,fy = final_paths[p['color']][idx]; pygame.draw.circle(SCREEN, p['color'], (fx,fy), 14); text(SCREEN, str(ti+1), fx-6, fy-8, WHITE)
            # dice display
            text(SCREEN, f"Dado: {dice}", W-140, 10, BLACK)
            pygame.display.flip()
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: return
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    if ai_flags[turn]:
                        continue
                    if wait_roll:
                        dice = roll(); message=f"Rolou {dice}"; wait_roll=False
                    else:
                        # attempt to move clicked token of current player
                        mx,my = ev.pos; moved=False
                        p=players[turn]
                        # check each token position for clicked
                        for ti,pos in enumerate(p['tokens']):
                            if pos==-1:
                                tx,ty = 60 + turn*200 + ti*30, H-120
                            elif 0<=pos<52:
                                tx,ty = ring[pos]
                            else:
                                idx = pos-100; tx,ty = final_paths[p['color']][idx]
                            if math.hypot(mx-tx, my-ty) <= 16:
                                moves = legal_moves(turn, dice)
                                chosen=None
                                for m in moves:
                                    if m[0]==ti: chosen=m; break
                                if chosen:
                                    apply_move(turn, ti, chosen[1])
                                    moved=True; break
                        if moved:
                            if dice!=6: turn = (turn+1)%num_players
                            wait_roll=True; message="Clique para rolar"
                        else:
                            message="Sem movimento com essa peça / clique para passar"
            # CPU processing
            if ai_flags[turn] and not wait_roll:
                moves = legal_moves(turn, dice)
                if moves:
                    chosen = random.choice(moves)
                    apply_move(turn, chosen[0], chosen[1])
                if dice!=6: turn = (turn+1)%num_players
                wait_roll=True; message="CPU jogou"
                pygame.time.delay(250)
            elif ai_flags[turn] and wait_roll:
                dice = roll(); wait_roll=False; message=f"CPU rolou {dice}"; pygame.time.delay(200)
            CLOCK.tick(FPS)
    except Exception:
        show_exception(traceback.format_exc())
        return

# ------------------ Erros: mostrar traceback na tela ------------------
def show_exception(tb):
    lines = tb.splitlines()
    while True:
        SCREEN.fill((30,30,30))
        text(SCREEN, "Erro! Copie o texto e me envie:", 10, 8, YELLOW)
        tail = lines[-20:]
        y = 40
        for ln in tail:
            text(SCREEN, ln, 10, y, WHITE, FONT); y += 18
        text(SCREEN, "Press ESC para voltar ao menu", 10, H-30, RED)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: return
        CLOCK.tick(10)

# ------------------ Inicia ------------------
if __name__ == "__main__":
    try:
        main_menu()
    except Exception:
        show_exception(traceback.format_exc())

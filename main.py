# SL-Fight main program
# V0.1 - 02/12/22

import pygame
import random as rd
import ClassPlayer
import ClassSolid
import ressources as rs
import config as cf
import vars as vr


def main():
    print("Main Started !")
    vr.time = pygame.time.get_ticks()
    time_fps = vr.time
    screen = PygameInit()
    clock = pygame.time.Clock()

    player1 = ClassPlayer.Player('tit2', '1', [200, 200])
    player2 = ClassPlayer.Player('arcane_mage', '2', [400, 200])
    players = [player1, player2]
    vr.players[str(player1.name)] = player1
    vr.players[str(player2.name)] = player2
    vr.players['player2'] = player2
    blocks = initBlocks(cf.arena)
    elements = [players, blocks]


    back = rs.backs['back1']

    running = True
    print("The game is about to start !")
    pygame.time.wait(2000)
    while running:
        clock.tick(cf.nb_fps)  # number of fps , update per seconds
        vr.nb_frames += 1
        if vr.nb_frames > 1000:
            vr.nb_frames = 1
            time_fps = vr.time
        fps = round((vr.nb_frames / (vr.time - time_fps + 1)) * 1000, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                vr.inputs["CLICK"] = True
                print(pygame.mouse.get_pos())
                pygame.time.wait(1000)
            else:
                vr.inputs["CLICK"] = False

        # ------------ Main Loop ------------ #
        getInputs()
        Calculation(elements)
        DisplayUpdate(screen, fps, elements, back)

    return


def Calculation(elements):
    vr.cursor = pygame.mouse.get_pos()
    vr.time = pygame.time.get_ticks()

    for key in vr.events.keys():
        vr.events[key].update()
        if vr.events[key].duration < vr.time - vr.events[key].start_time:
            vr.events_del_keys.append(key)
    for key in vr.events_del_keys:
        try:
            del vr.events[key]
        except:
            pass
    vr.events_del_keys = []

    for elt in elements[0]:
        elt.update()
        if elt.state == 'dead':
            elements[0].remove(elt)
            del vr.solids[elt.num]

    return

# //// ----------------- PYGAME MANAGEMENT ---------------- \\\\ #


def DisplayUpdate(screen, fps, elements, back):
    if isinstance(back, pygame.Surface):
        screen.blit(pygame.transform.scale(back, (cf.screenx, cf.screeny)), [0, 0])
    else:
        screen.fill(pygame.Color('NavyBlue'))

    for key in vr.solids.keys():
        draw_hitbox(screen, vr.solids[key].hitbox)

    for elt in elements[0]:
        screen.blit(elt.visual, [elt.getx(), elt.gety()])
        #Text(elt.name, elt.coord, 12, "red", screen)
        Text(elt.state, elt.coord, 12, "red", screen)
        for detector in elt.detectors:
            screen.blit(detector.visual, detector.coord_draw())
        pygame.draw.line(screen, "grey", elt.getCoordHealthBar()[0], [elt.getCoordHealthBar()[1][0] + elt.size[0], elt.getCoordHealthBar()[1][1]], 3)
        pygame.draw.line(screen, "red", elt.getCoordHealthBar()[0], [elt.getCoordHealthBar()[1][0] + elt.size[0]*((elt.getHealth()[0])/(elt.getHealth()[1])), elt.getCoordHealthBar()[1][1]], 3)

    for key in vr.events.keys():
        try:
            screen.blit(vr.events[key].visual, [vr.events[key].getx(), vr.events[key].gety()])
            draw_hitbox(screen, vr.events[key].hitbox)
            for detector in vr.events[key].detectors:
                screen.blit(detector.visual, detector.coord_draw())
        except:
            pass

    Text(("FPS : " + str(fps)), (20, 20), 20, "grey", screen)
    pygame.display.update()
    return


def PygameInit():
    pygame.init()
    logo = pygame.image.load("ressources/visuals/GUI/logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("SL-Fight")
    screen = pygame.display.set_mode((cf.screenx, cf.screeny))
    screen.fill(pygame.Color('NavyBlue'))
    return screen


def initBlocks(arena):
    blocks = []
    for block in rs.arena_blocks[arena]:
        solid = ClassSolid.Block(block[0], block[1], 'wall', vr.solid_num)
        vr.solid_num += 1
        blocks.append(solid)
        vr.solids[vr.solid_num] = solid
    return blocks


# //// ----------------- TOOLS ---------------- \\\\ #

def draw_hitbox(screen, hitbox):
    width = hitbox[1][0] - hitbox[0][0]
    pygame.draw.line(screen, "red", hitbox[0], [hitbox[0][0] + width, hitbox[0][1]])
    pygame.draw.line(screen, "red", [hitbox[0][0] + width, hitbox[0][1]], hitbox[1])
    pygame.draw.line(screen, "red", hitbox[1], [hitbox[1][0] - width, hitbox[1][1]], )
    pygame.draw.line(screen, "red", [hitbox[1][0] - width, hitbox[1][1]], hitbox[0])
    return

def getInputs():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        vr.inputs["RIGHT"] = True
    else:
        vr.inputs["RIGHT"] = False
    if keys[pygame.K_LEFT]:
        vr.inputs["LEFT"] = True
    else:
        vr.inputs["LEFT"] = False
    if keys[pygame.K_UP]:
        vr.inputs["UP"] = True
    else:
        vr.inputs["UP"] = False
    if keys[pygame.K_DOWN]:
        vr.inputs["DOWN"] = True
    else:
        vr.inputs["DOWN"] = False
    if keys[pygame.K_SPACE]:
        vr.inputs["SPACE"] = True
    else:
        vr.inputs["SPACE"] = False
    if keys[pygame.K_ESCAPE]:
        vr.inputs["ESCAPE"] = True
    else:
        vr.inputs["ESCAPE"] = False
    if keys[pygame.K_i]:
        vr.inputs["I"] = True
    else:
        vr.inputs["I"] = False
    if keys[pygame.K_o]:
        vr.inputs["O"] = True
    else:
        vr.inputs["O"] = False
    if keys[pygame.K_u]:
        vr.inputs["U"] = True
    else:
        vr.inputs["U"] = False
    if keys[pygame.K_e]:
        vr.inputs["E"] = True
    else:
        vr.inputs["E"] = False
    if keys[pygame.K_r]:
        vr.inputs["R"] = True
    else:
        vr.inputs["R"] = False
    if keys[pygame.K_f]:
        vr.inputs["F"] = True
    else:
        vr.inputs["F"] = False
    if keys[pygame.K_z]:
        vr.inputs["Z"] = True
    else:
        vr.inputs["Z"] = False
    if keys[pygame.K_q]:
        vr.inputs["Q"] = True
    else:
        vr.inputs["Q"] = False
    if keys[pygame.K_s]:
        vr.inputs["S"] = True
    else:
        vr.inputs["S"] = False
    if keys[pygame.K_d]:
        vr.inputs["D"] = True
    else:
        vr.inputs["D"] = False
    if keys[pygame.K_g]:
        vr.inputs["G"] = True
    else:
        vr.inputs["G"] = False
    if keys[pygame.K_l]:
        vr.inputs["L"] = True
    else:
        vr.inputs["L"] = False


def Text(msg, coord, size, color, screen):  # blit to the screen a text
    TextColor = pygame.Color(color)  # set the color of the text
    font = pygame.font.Font("/Users/arthur/PycharmProjects/QForAChampion/venv/ressources/miscellaneous/font.ttf", size)  # set the font
    return screen.blit(font.render(msg, True, TextColor), coord)  # return and blit the text on the screen


def getRndPos():
    return [rd.randint(0, cf.screenx), rd.randint(0, cf.screeny)]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

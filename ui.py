import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

prev_l = pygame.Vector2(0, 0)
prev_r = pygame.Vector2(0, 0)


def get_glove_size(
    elbow_angle_deg,
    base_glove_size,
    min_angle=30,
    max_angle=180,
    min_scale=1.5,
    max_scale=0.2,
    smooth=True,
    alpha=0.3,
    _state={},
):
    angle = max(min_angle, min(max_angle, elbow_angle_deg))
    t = (angle - min_angle) / (max_angle - min_angle)
    scale = min_scale + t * (max_scale - min_scale)

    if smooth:
        prev = _state.get("scale", scale)
        scale = alpha * scale + (1 - alpha) * prev
        _state["scale"] = scale

    return base_glove_size * scale


def render(xl, yl, elbow_anglel, xr, yr, elbow_angler):
    global prev_l, prev_r

    target_l = pygame.Vector2(xl, yl)
    target_r = pygame.Vector2(xr, yr)

    dt = clock.tick(30) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    speed = 5
    prev_l = prev_l.lerp(target_l, min(speed * dt, 1))
    prev_r = prev_r.lerp(target_r, min(speed * dt, 1))

    screen.fill((0, 0, 0))

    glove_sizel = get_glove_size(elbow_anglel, 40)
    pygame.draw.circle(screen, "red", prev_l, int(glove_sizel))

    glove_sizer = get_glove_size(elbow_angler, 40)
    pygame.draw.circle(screen, "red", prev_r, int(glove_sizer))

    pygame.display.flip()

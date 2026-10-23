"""Exercise the actual bundled resources and game modules."""
import hashlib
import json
import os
from pathlib import Path
import traceback


def verify(report_file):
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    report_path = Path(report_file).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {'passed': False, 'checks': []}
    try:
        import pygame
        from asset_loader import PROJECT_DIR, resource_path, load_asset_image
        from starting_menu import StartMenu
        from main_menu import MainMenu
        from characters_menu import Characters_menu
        from credits import Credits
        from gameplay import play_game
        import g_var

        pygame.init()
        screen = pygame.display.set_mode((900, 400))
        manifest = json.loads((PROJECT_DIR / 'asset-manifest.json').read_text(encoding='utf-8'))
        images = fonts = sounds = 0
        for relative, expected in manifest.items():
            path = Path(resource_path(relative))
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative
            if path.suffix.lower() == '.png':
                load_asset_image(relative).convert_alpha()
                images += 1
            elif path.suffix.lower() == '.ttf':
                pygame.font.Font(str(path), 25).render('中文測試', True, 'white')
                fonts += 1
            elif path.suffix.lower() in ('.mp3', '.wav', '.ogg'):
                pygame.mixer.Sound(str(path))
                sounds += 1
        report.update(resources=len(manifest), images=images, fonts=fonts, sounds=sounds)
        report['checks'].append('Every resource hash matches; all images, fonts and audio decoded')
        for cls in (StartMenu, MainMenu, Characters_menu, Credits):
            cls(screen).draw()
            pygame.image.save(screen, str(report_path.parent / (cls.__name__ + '.png')))
            report['checks'].append(cls.__name__ + ' rendered')

        original_get = pygame.event.get
        original_custom_type = pygame.event.custom_type
        original_load = pygame.image.load
        seen_images = set()
        def tracked_load(path, *args):
            seen_images.add(str(Path(path).relative_to(PROJECT_DIR)).replace('\\', '/'))
            return original_load(path, *args)
        pygame.image.load = tracked_load
        for level in range(1, 6):
            pygame.init()
            screen = pygame.display.set_mode((900, 400))
            custom_types = []
            def custom_type():
                value = original_custom_type()
                custom_types.append(value)
                return value
            frames = [0]
            def events():
                frames[0] += 1
                if frames[0] == 2:
                    g_var.player_money = 10000
                    # Four units, meteor and enemy spawn events, registered by play_game.
                    assert len(custom_types) == 6, custom_types
                    return [pygame.event.Event(value) for value in custom_types]
                if frames[0] == 30:
                    pygame.image.save(screen, str(report_path.parent / f'level-{level}.png'))
                    return [pygame.event.Event(pygame.QUIT)]
                return original_get()
            pygame.event.custom_type = custom_type
            pygame.event.get = events
            try:
                play_game(screen, 'gameplay' + str(level))
            except SystemExit:
                assert frames[0] == 30
            finally:
                pygame.event.custom_type = original_custom_type
                pygame.event.get = original_get
            report['checks'].append(f'Level {level}: units, meteor and enemy spawned; 29 event loops rendered')
        pygame.image.load = original_load
        report['gameplay_images_loaded'] = sorted(seen_images)
        # Import the actual normal entry point, including its music startup.
        pygame.init()
        pygame.event.get = lambda: [pygame.event.Event(pygame.QUIT)]
        try:
            import main
        except SystemExit:
            pass
        finally:
            pygame.event.get = original_get
        report['checks'].append('Normal main entry initialized with background music')
        report['passed'] = True
        pygame.quit()
    except Exception:
        report['error'] = traceback.format_exc()
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0 if report['passed'] else 1

"""Launch the game or run the packaged resource verification."""
import sys

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--verify-assets':
        from packaged_checks import verify
        raise SystemExit(verify(sys.argv[2]))
    import main

#!/usr/bin/env python

import subprocess
import sys

class VersionManager:
    def get_current_version(self, ) -> str:
        result = subprocess.run(
            ["uv", "version", "--short"], capture_output=True, text=True
        )

        return (
            result.stdout.strip()
            if result.returncode == 0
            else sys.exit(result.returncode)
        )

    def is_stable(self, current_ver) -> bool:
        current_ver = self.get_current_version()
        return True if all(part.isdigit() for part in current_ver.split(".")) else False


def main() -> bool:
    vm = VersionManager()
    return vm.is_stable()
    
if __name__ == "__main__":
    main()

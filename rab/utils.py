#!/usr/bin/env python3

import asyncio
import logging
from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, Optional, Sequence, Tuple, Union


LOG = logging.getLogger(__name__)


async def gen_check_output(
    cmd: Sequence[str],
    timeout: Union[int, float] = 30,
    env: Optional[Dict[str, str]] = None,
    cwd: Optional[Path] = None,
) -> Tuple[Optional[bytes], Optional[bytes]]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=env,
        cwd=cwd,
    )
    try:
        (stdout, stderr) = await asyncio.wait_for(process.communicate(), timeout)
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise

    if process.returncode != 0:
        cmd_str = " ".join(cmd)
        raise CalledProcessError(
            process.returncode or -1, cmd_str, output=stdout, stderr=stderr
        )

    return (stdout, stderr)

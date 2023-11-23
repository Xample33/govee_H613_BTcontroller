<h1 align="center"> Control govee lights with python </h1>

<h3 align="center"> Simple python package to control govee H613B (and technically more) led strip with python <h3>

<p align="center">  
  <a href="https://github.com/astral-sh/ruff"><img alt="Ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>
  <a href="https://pypi.org/project/govee-H613-BTcontroller"><img alt="PyPI - Version" src="https://badgen.net/pypi/v/govee-H613-BTcontroller"></a>
  <a href="https://pypi.org/project/govee-H613-BTcontroller"><img alt="PyPI - Python Version" src="https://badgen.net/pypi/python/govee-H613-BTcontroller"></a>
  <a href="https://pypi.org/project/govee-H613-BTcontroller"><img alt="PyPI - Downloads" src="https://badgen.net/pypi/dm/govee-H613-BTcontroller"></a>
  <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FXample33%2Fgovee_H613_BTcontroller&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false">
</p>

## Installation

```
pip3 install govee_H613_BTcontroller
```

## Example

```python
import asyncio
from govee_H613_BTcontroller import GoveeController

async def main():
    device = GoveeController('A4:C1:38:35:97:24')
    device = await device.connect()
    
    await device.turn_on()
    
    await device.set_color('red')
    await device.set_brightness(255)
    await asyncio.sleep(3)
    await device.set_color('green')
    
    await device.turn_off(smooth=True)
    await device.disconnect()
    
if __name__ == '__main__':
    asyncio.run(main())
```

## Contributing
Contributions are welcome! Feel free to open a PR.


## License
This project is licensed under the MIT License.


> ☆ If you like the project, please leave a star, is free!

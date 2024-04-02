# Nose-Pick Detection with MediaPipe
This project uses the MediaPipe library to detect when a person is touching or picking their nose. If the gesture is detected, it simulates pausing or playing a YouTube video running on the local machine.

Este projeto usa a biblioteca MediaPipe para detectar quando uma pessoa está tocando ou cutucando seu nariz. Se o gesto é detectado, o projeto simula uma pausa ou play em um vídeo do YouTube em execução na máquina local.

**Languages / Idiomas**
- [English](#english)
- [Português](#português)

---

## English

### Requirements

- Python 3.6+
- Mediapipe
- OpenCV
- PyAutoGUI
- A webcam

### Environment Setup

It is recommended to use a virtual environment to install and run this project.

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
## File Structure
- main.py: The main script for real-time detection using the webcam.
- map-landmarks-in-face.py: A utility script for marking and visualizing face landmarks on a static image.
- requirements.txt: Lists all dependencies required to run the scripts.

## How to Run
### Real-Time Detection
Run main.py to start real-time detection. Ensure your webcam is connected and operational.

```sh
python main.py
```

## Landmark Mapping
Run map-landmarks-in-face.py to map face landmarks on a static image. Replace 'images/image.png' with the path to your image.

```sh
python map-landmarks-in-face.py
```

## Notes
- The script simulates key presses, which can interact with programs other than video players. Ensure the system focus is on the desired video before running the script.
- Adjustments may be necessary for use with other platforms or customized settings.

## Contributions
Contributions are welcome! If you have improvements or corrections, please fork the repository and submit a Pull Request.

---

## Português

## Requisitos

- Python 3.6+
- Mediapipe
- OpenCV
- PyAutoGUI
- Uma webcam

## Configuração do Ambiente

Recomenda-se usar um ambiente virtual para instalar e executar este projeto.

```sh
python3 -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Estrutura de Arquivos
main.py: Script principal que executa a detecção em tempo real usando a webcam.
map-landmarks-in-face.py: Utilitário para marcar e visualizar as landmarks do rosto em uma imagem estática.
requirements.txt: Lista todas as dependências necessárias para executar os scripts.

## Como Executar
### Detecção em Tempo Real
Para iniciar a detecção em tempo real, execute o script main.py. Certifique-se de que sua webcam esteja conectada e funcionando.

```sh
python main.py
```

## Mapeamento de Landmarks
Para mapear as landmarks do rosto em uma imagem estática, execute o script map-landmarks-in-face.py. Certifique-se de substituir 'images/image.png' pelo caminho da imagem que deseja processar.

```sh
python map-landmarks-in-face.py
```

## Funcionalidades
- Detecta o gesto de cutucar o nariz em tempo real usando a webcam.
- Pausa e dá play em vídeos do YouTube controlando o teclado com a biblioteca PyAutoGUI.
- Visualiza as landmarks do rosto em uma imagem estática.

## Notas
- Este script simula pressionamentos de tecla e, portanto, pode interagir com outros programas além dos players de vídeo. Certifique-se de que o foco do sistema esteja no vídeo desejado antes de executar o script.
- O main.py foi configurado para funcionar com o layout e atalhos de teclado padrão do YouTube. Pode ser necessário ajustes para uso com outras plataformas ou configurações personalizadas.

## Contribuições
Contribuições são bem-vindas! Se você tem melhorias ou correções, por favor, faça um fork do repositório e envie um Pull Request.

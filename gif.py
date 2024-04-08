import os
import sys
import imageio
from glob import glob

def convertFiles(input_dir, output_dir, output_format):
    try:
        # Verifica se o diretório de entrada existe
        if not os.path.exists(input_dir):
            raise FileNotFoundError("O diretório de entrada não existe.")

        # Cria o diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)

        # Lista todos os arquivos de vídeo no diretório de entrada
        video_files = glob(os.path.join(input_dir, '*.mp4')) + glob(os.path.join(input_dir, '*.avi'))

        # Itera sobre os arquivos de vídeo
        for inputpath in video_files:
            # Gera o nome de arquivo de saída com base no diretório de saída e no nome do arquivo de entrada
            outputpath = os.path.join(output_dir, os.path.splitext(os.path.basename(inputpath))[0] + output_format)
            print(f"Convertendo {inputpath} para {outputpath}")

            # Abre o arquivo de entrada para leitura
            with imageio.get_reader(inputpath) as reader:
                # Obtém a taxa de frames por segundo do vídeo
                fps = reader.get_meta_data()['fps']

                # Abre o arquivo de saída para escrita
                with imageio.get_writer(outputpath, fps=fps) as writer:
                    # Obtém o número total de frames no vídeo
                    total_frames = len(reader)
                    # Itera sobre cada frame do vídeo
                    for i, im in enumerate(reader):
                        # Atualiza o progresso da conversão
                        sys.stdout.write(f"\rProcessando frame {i+1}/{total_frames}")
                        sys.stdout.flush()
                        # Adiciona o frame ao arquivo de saída
                        writer.append_data(im)
                    
                    # Informa sobre a conclusão da conversão para o arquivo atual
                    print(f"\nConversão concluída com sucesso para {os.path.basename(inputpath)}")
    except FileNotFoundError as e:
        # Captura e trata o erro se o diretório de entrada não existir
        print(f"\nErro: {str(e)}")
    except Exception as e:
        # Captura e trata outros erros desconhecidos durante o processo de conversão
        print(f"\nErro desconhecido: {str(e)}")

# Exemplo de uso:
input_directory = os.path.dirname(__file__)
output_directory = os.path.join(input_directory, 'output')  # Output em um diretório 'output' dentro do diretório de entrada
convertFiles(input_directory, output_directory, '.gif')

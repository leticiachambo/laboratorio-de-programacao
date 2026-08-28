# Dataset — DogVision

## Fonte

[Stanford Dogs Dataset](http://vision.stanford.edu/aditya86/ImageNetDogs/) —
120 raças de cães, imagens extraídas do ImageNet, já acompanhadas de
anotações de bounding box no formato Pascal VOC (XML).

## Como obter os dados

1. Acesse http://vision.stanford.edu/aditya86/ImageNetDogs/ e baixe:
   - `images.tar` (imagens)
   - `annotation.tar` (anotações Pascal VOC)
2. Extraia ambos os arquivos dentro de `dataset/raw/`, mantendo a estrutura:

   ```
   dataset/raw/
     Images/
       n02085620-Chihuahua/
       n02085782-Japanese_spaniel/
       ...
     Annotation/
       n02085620-Chihuahua/
       n02085782-Japanese_spaniel/
       ...
   ```

3. **Não versionar os dados brutos nem o dataset processado no Git** — ambos
   já estão listados no `.gitignore` da raiz do repositório, pois somam
   vários gigabytes. Cada integrante deve baixar o dataset localmente.

## Como gerar o conjunto anotado e particionado

```bash
pip install -r ../requirements.txt
python prepare_dataset.py
```

Por padrão, o script seleciona 12 raças com quantidade equilibrada de
imagens (ver `DEFAULT_BREEDS` em `prepare_dataset.py`), converte as
anotações de Pascal VOC para o formato YOLO e gera a partição
estratificada 70% treino / 15% validação / 15% teste em
`dataset/processed/`.

Para escolher outro conjunto de raças ou outras proporções:

```bash
python prepare_dataset.py --racas Beagle Pug Rottweiler --train 0.8 --val 0.1 --test 0.1
```

## Saída gerada

```
dataset/processed/
  train/images/  train/labels/
  val/images/    val/labels/
  test/images/   test/labels/
  classes.txt        # uma raça por linha, na ordem usada como class_id
  raca_seed.csv       # dados prontos para popular a tabela `raca` (database/schema.sql)
```

Após executar o script, preencha a tabela de estatísticas da Seção 4.5 do
documento `docs/02_Modelagem_Dados_e_Casos_de_Uso.docx` com os números
exibidos ao final da execução.

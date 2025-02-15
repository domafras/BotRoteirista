import google.generativeai as genai

def detectar_produtos(chave, imagem):
    genai.configure(api_key=chave)
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    prompt = '''Analise os produtos desta imagem e forneça uma descrição sucinta de cada um.
    
    Para cada produto, caso identificado, liste:
    - Nome do produto (fragrância, aroma, modelo)
    - Marca (se visível)
    - Quantidade/Volume (se visível)

    Nenhum texto adicional deve ser gerado como resposta além dos próprios itens.
    Formate a saída como uma lista separada por ponto e vírgula (,)
    
    Exemplo:
    Base Mate (Boca Rosa Beauty), 30ml - Base líquida com acabamento matte para pele,
    Batom Líquido (Boca Rosa Beauty), 4ml - Batom vermelho de longa duração
    '''

    resposta = modelo.generate_content([prompt, imagem])
    produtos = resposta.text.split(",")
    
    return produtos

def possiveis_roteiros(chave, produtos):
    genai.configure(api_key=chave)
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f'''Considerando a seguinte lista de produtos, gere uma lista de roteiros para vídeos curtos (TikTok, Reels, Shorts) que tenham os produtos como o tema central.
    Os roteiros devem tentar incluir a maior parte dos produtos.

    Gere apenas uma lista com o título das idéias de conteúdo, separados por vírgula.

    # Lista de produtos
    {produtos}

    # Exemplo de saída
    Roteiro 1, Roteiro 2, Roteiro 3 (máximo 10)
    '''

    resposta = modelo.generate_content(prompt)
    roteiros = resposta.text.split(",")
    
    return roteiros

def roteiro_completo(chave, produtos, roteiro, estilo):
    genai.configure(api_key=chave)
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    estilos = {
        'Informal': 'tom descontraído e conversacional, linguagem do dia a dia',
        'Divertido': 'tom bem-humorado, pode incluir elementos cômicos e trends',
        'Informativo': 'foco em dados, benefícios e características técnicas',
        'Publi': 'tom comercial sutíl, destacando diferenciais e call-to-action'
    }

    prompt = f'''Crie um guia criativo para o vídeo: "{roteiro}".
    Estilo do conteúdo: {estilos[estilo]}

    Inclua a maior quantidade possível dos produtos (itens identificados) da lista de produtros

    a) Produtos identificados: {produtos}
    - Nome do produto, fragrância (se visível)
    - Marca (se visível)
    - Quantidade/Volume (se visível)
    Nenhum texto adicional deve ser gerado como resposta além dos próprios itens.


    b) Mensagens Importantes
    - Liste 3 pontos principais que devem ser abordados

    c) Estrutura Sugerida
    - Início: qual gancho ou abertura pode chamar atenção (1-2 linha)
    - Meio: principais pontos a serem desenvolvidos (1-2 linhas)
    - Fim: que tipo de conclusão ou call-to-action usar (1-2 linhas)

    d) Elementos Criativos
    - Ideias de enquadramento ou cenário
    - Ideias de roupas ou maquiagens para utilizar nessa gravação
    - Possíveis músicas ou sons que combinem com o contexto do vídeo e itens abordados

    e) Produtos similares
    - Listar produtos similares (máximo 2, mostrar em tópico - para cada), que sejam parecidos com a lista de {produtos} identificadas na imagem. (nome, marca, quantidade)

    f) Palavras-chave
    - Sugestões de palavras-chave ou hashtags que estejam dentro do contexto e em tendência
    '''

    resposta = modelo.generate_content(prompt)
    
    return resposta.text


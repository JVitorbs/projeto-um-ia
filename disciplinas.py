PRIMEIRO_SEMESTRE_FIXO = [
    "ECT3101",  # MATEMATICA BASICA E MODELAGEM
    "ECT3102",  # ALGEBRA MATRICIAL E VETORIAL
    "ECT3103",  # METODOLOGIA CIENTIFICA, TECNOLOGICA E EMPREENDEDORA
    "ECT3104",  # LOGICA DE PROGRAMACAO
    "ECT3105",  # PRATICAS DE LEITURA E ESCRITA I
    "ECT3106",  # CIENCIA, TECNOLOGIA E SOCIEDADE
    "ECT3107",  # INTRODUCAO AS CIENCIAS E TECNOLOGIA
    "ECT3203",  # AMBIENTE E DESENVOLVIMENTO
]


disciplinas = {
    # 1o nivel (fixo)
    "ECT3101": {"nome": "MATEMATICA BASICA E MODELAGEM", "carga": 60, "dificuldade": 0.5, "prereq": [], "tipo": "obrigatoria"},
    "ECT3102": {"nome": "ALGEBRA MATRICIAL E VETORIAL", "carga": 60, "dificuldade": 0.6, "prereq": [], "tipo": "obrigatoria"},
    "ECT3103": {"nome": "METODOLOGIA CIENTIFICA, TECNOLOGICA E EMPREENDEDORA", "carga": 30, "dificuldade": 0.3, "prereq": [], "tipo": "obrigatoria"},
    "ECT3104": {"nome": "LOGICA DE PROGRAMACAO", "carga": 60, "dificuldade": 0.4, "prereq": [], "tipo": "obrigatoria"},
    "ECT3105": {"nome": "PRATICAS DE LEITURA E ESCRITA I", "carga": 30, "dificuldade": 0.3, "prereq": [], "tipo": "obrigatoria"},
    "ECT3106": {"nome": "CIENCIA, TECNOLOGIA E SOCIEDADE", "carga": 30, "dificuldade": 0.3, "prereq": [], "tipo": "obrigatoria"},
    "ECT3107": {"nome": "INTRODUCAO AS CIENCIAS E TECNOLOGIA", "carga": 30, "dificuldade": 0.3, "prereq": [], "tipo": "obrigatoria"},
    "ECT3203": {"nome": "AMBIENTE E DESENVOLVIMENTO", "carga": 60, "dificuldade": 0.4, "prereq": [], "tipo": "obrigatoria"},

    # 2o nivel
    "DCA3206": {"nome": "MATEMATICA DISCRETA", "carga": 60, "dificuldade": 0.6, "prereq": ["ECT3104"], "tipo": "obrigatoria"},
    "ECT3201": {"nome": "LINGUAGEM DE PROGRAMACAO", "carga": 60, "dificuldade": 0.5, "prereq": ["ECT3104"], "tipo": "obrigatoria"},
    "ECT3202": {"nome": "ALGEBRA LINEAR", "carga": 60, "dificuldade": 0.6, "prereq": ["ECT3102"], "tipo": "obrigatoria"},
    "ECT3204": {"nome": "MODELAGEM DO MUNDO FISICO I", "carga": 30, "dificuldade": 0.5, "prereq": ["ECT3203"], "tipo": "obrigatoria"},
    "ECT3205": {"nome": "PRATICAS DE LEITURA E ESCRITA II", "carga": 30, "dificuldade": 0.3, "prereq": ["ECT3105"], "tipo": "obrigatoria"},
    "ECT3207": {"nome": "CALCULO DIFERENCIAL E INTEGRAL I", "carga": 90, "dificuldade": 0.8, "prereq": ["ECT3101"], "tipo": "obrigatoria"},
    "ECT3308": {"nome": "CIENCIA, TECNOLOGIA E SOCIEDADE II", "carga": 30, "dificuldade": 0.3, "prereq": ["ECT3106"], "tipo": "obrigatoria"},

    # 3o nivel
    "DCA3301": {"nome": "SISTEMAS DIGITAIS", "carga": 75, "dificuldade": 0.6, "prereq": ["ECT3202"], "tipo": "obrigatoria"},
    "DCA3303": {"nome": "PROGRAMACAO AVANCADA", "carga": 90, "dificuldade": 0.7, "prereq": ["ECT3201"], "tipo": "obrigatoria"},
    "ECT3302": {"nome": "CALCULO DIFERENCIAL E INTEGRAL II", "carga": 60, "dificuldade": 0.8, "prereq": ["ECT3207"], "tipo": "obrigatoria"},
    "ECT3304": {"nome": "PROBABILIDADE E ESTATISTICA", "carga": 60, "dificuldade": 0.6, "prereq": ["ECT3207"], "tipo": "obrigatoria"},
    "ECT3305": {"nome": "PRATICAS DE LEITURA EM INGLES", "carga": 30, "dificuldade": 0.3, "prereq": ["ECT3205"], "tipo": "obrigatoria"},
    "ECT3306": {"nome": "FUNDAMENTOS DA MECANICA", "carga": 60, "dificuldade": 0.6, "prereq": ["ECT3204"], "tipo": "obrigatoria"},

    # 4o nivel
    "DCA3402": {"nome": "MODELAGEM E ANALISE LINEAR DE SISTEMAS", "carga": 60, "dificuldade": 0.7, "prereq": ["ECT3302"], "tipo": "obrigatoria"},
    "DCA3404": {"nome": "ARQUITETURA DE COMPUTADORES", "carga": 60, "dificuldade": 0.6, "prereq": ["DCA3301"], "tipo": "obrigatoria"},
    "ECT3303": {"nome": "GESTAO E ECONOMIA DA CIENCIA, TECNOLOGIA E INOVACAO", "carga": 60, "dificuldade": 0.4, "prereq": ["ECT3308"], "tipo": "obrigatoria"},
    "ECT3401": {"nome": "COMPUTACAO NUMERICA", "carga": 60, "dificuldade": 0.6, "prereq": ["ECT3302", "ECT3202"], "tipo": "obrigatoria"},
    "ECT3403": {"nome": "MODELAGEM DO MUNDO FISICO II", "carga": 30, "dificuldade": 0.5, "prereq": ["ECT3204"], "tipo": "obrigatoria"},

    # 5o e 6o niveis
    "DCA3501": {"nome": "CIENCIA DE DADOS", "carga": 60, "dificuldade": 0.7, "prereq": ["ECT3304", "DCA3303"], "tipo": "obrigatoria"},
    "DCA3502": {"nome": "SINAIS E SISTEMAS", "carga": 60, "dificuldade": 0.8, "prereq": ["ECT3302", "ECT3306"], "tipo": "obrigatoria"},
    "DCA3503": {"nome": "ALGORITMOS E ESTRUTURAS DE DADOS I", "carga": 60, "dificuldade": 0.7, "prereq": ["DCA3303"], "tipo": "obrigatoria"},
    "ECT3511": {"nome": "FUNDAMENTOS DE CIRCUITOS E SISTEMAS CONTROLADOS", "carga": 54, "dificuldade": 0.7, "prereq": ["DCA3301"], "tipo": "obrigatoria"},
    "ECT3622": {"nome": "FUNDAMENTOS DO ELETROMAGNETISMO", "carga": 60, "dificuldade": 0.7, "prereq": ["ECT3306"], "tipo": "obrigatoria"},
    "DCA3504": {"nome": "OTIMIZACAO DE SISTEMAS", "carga": 60, "dificuldade": 0.7, "prereq": ["ECT3401"], "tipo": "obrigatoria"},
    "DCA3505": {"nome": "SISTEMAS OPERACIONAIS", "carga": 60, "dificuldade": 0.7, "prereq": ["DCA3404", "DCA3503"], "tipo": "obrigatoria"},
    "DCA3506": {"nome": "ELETRONICA", "carga": 75, "dificuldade": 0.7, "prereq": ["ECT3511"], "tipo": "obrigatoria"},

    # 6o e 7o niveis
    "DCA3601": {"nome": "ANALISE DE SISTEMAS DE CONTROLE", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3402", "DCA3502"], "tipo": "obrigatoria"},
    "DCA3602": {"nome": "PROCESSAMENTO DIGITAL DE SINAIS", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3502"], "tipo": "obrigatoria"},
    "DCA3603": {"nome": "ENGENHARIA DE SOFTWARE", "carga": 45, "dificuldade": 0.5, "prereq": ["DCA3503"], "tipo": "obrigatoria"},
    "DCA3604": {"nome": "BANCO DE DADOS", "carga": 45, "dificuldade": 0.5, "prereq": ["DCA3503"], "tipo": "obrigatoria"},
    "DCA3605": {"nome": "REDES DE COMPUTADORES", "carga": 60, "dificuldade": 0.6, "prereq": ["DCA3404", "DCA3505"], "tipo": "obrigatoria"},
    "DCA3606": {"nome": "INTELIGENCIA ARTIFICIAL", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3501", "DCA3504"], "tipo": "obrigatoria"},
    "ECT3517": {"nome": "CIENCIAS E TECNOLOGIAS APLICADAS 3", "carga": 30, "dificuldade": 0.4, "prereq": ["ECT3303"], "tipo": "obrigatoria"},

    # 7o nivel
    "DCA3701": {"nome": "PROJETO DE SISTEMAS DE CONTROLE", "carga": 90, "dificuldade": 0.8, "prereq": ["DCA3601"], "tipo": "obrigatoria"},
    "DCA3702": {"nome": "ALGORITMOS E ESTRUTURAS DE DADOS II", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3503"], "tipo": "obrigatoria"},
    "DCA3703": {"nome": "PROGRAMACAO PARALELA", "carga": 45, "dificuldade": 0.7, "prereq": ["DCA3505", "DCA3503"], "tipo": "obrigatoria"},
    "DCA3704": {"nome": "SISTEMAS DISTRIBUIDOS", "carga": 45, "dificuldade": 0.7, "prereq": ["DCA3605", "DCA3505"], "tipo": "obrigatoria"},
    "DCA3705": {"nome": "AUTOMATOS E LINGUAGENS FORMAIS", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3206", "DCA3503"], "tipo": "obrigatoria"},
    "DCA3706": {"nome": "SISTEMAS EMBARCADOS", "carga": 60, "dificuldade": 0.7, "prereq": ["DCA3404", "DCA3506", "DCA3505"], "tipo": "obrigatoria"},

    # 8o, 9o e 10o niveis
    "DCA3801": {"nome": "PROJETO INTEGRADO", "carga": 120, "dificuldade": 0.7, "prereq": ["DCA3701", "DCA3706", "DCA3603", "DCA3604"], "tipo": "obrigatoria"},
    "ECP3901": {"nome": "TRABALHO DE CONCLUSAO DE CURSO", "carga": 160, "dificuldade": 0.6, "prereq": ["DCA3801"], "tipo": "obrigatoria"},
    "ECP3902": {"nome": "ESTAGIO OBRIGATORIO", "carga": 160, "dificuldade": 0.5, "prereq": ["DCA3801"], "tipo": "obrigatoria"},

    # Optativas
    "DCA0114": {"nome": "COMPUTACAO GRAFICA", "carga": 60, "dificuldade": 0.6, "prereq": ["ECT3202", "DCA3503"], "tipo": "optativa"},
    "DCA0132": {"nome": "ENGENHARIA DE DADOS", "carga": 60, "dificuldade": 0.7, "prereq": ["DCA3604", "DCA3501"], "tipo": "optativa"},
    "DCA0133": {"nome": "APRENDIZAGEM DE MAQUINA E MINERACAO DE DADOS", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3606"], "tipo": "optativa"},
    "DCA0306": {"nome": "INTELIGENCIA ARTIFICIAL EMBARCADA", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3706", "DCA3606"], "tipo": "optativa"},
    "DCA0402": {"nome": "SEGURANCA DE REDES DE COMPUTADORES", "carga": 60, "dificuldade": 0.7, "prereq": ["DCA3605"], "tipo": "optativa"},
    "DCA0440": {"nome": "SISTEMAS ROBOTICOS AUTONOMOS", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3706", "DCA3601"], "tipo": "optativa"},
    "DCA0445": {"nome": "PROCESSAMENTO DIGITAL DE IMAGENS", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3602"], "tipo": "optativa"},
    "ECT3694": {"nome": "APRENDIZADO DE MAQUINA", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3606"], "tipo": "optativa"},
    "ECT3695": {"nome": "APRENDIZADO PROFUNDO (DEEP LEARNING)", "carga": 60, "dificuldade": 0.9, "prereq": ["ECT3694"], "tipo": "optativa"},
    "ECT3701": {"nome": "PROJETOS COM IOT", "carga": 60, "dificuldade": 0.7, "prereq": ["DCA3706"], "tipo": "optativa"},
    "ECT3709": {"nome": "VISAO COMPUTACIONAL", "carga": 60, "dificuldade": 0.8, "prereq": ["ECT3694"], "tipo": "optativa"},
    "IMD1107": {"nome": "PROCESSAMENTO DE LINGUAGEM NATURAL", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3606"], "tipo": "optativa"},
    "IMD1114": {"nome": "APRENDIZADO PROFUNDO", "carga": 60, "dificuldade": 0.9, "prereq": ["DCA3606"], "tipo": "optativa"},
    "IMD1115": {"nome": "PROCESSAMENTO DIGITAL DE IMAGENS", "carga": 60, "dificuldade": 0.8, "prereq": ["DCA3602"], "tipo": "optativa"},
}

import numpy as np
import skfuzzy as fz
from skfuzzy import control as cf

# Definição das variáveis linguísticas
organizacao = cf.Antecedent(np.arange(0, 11, 1), 'organizacao')
atendimento = cf.Antecedent(np.arange(0, 11, 1), 'atendimento')
conforto = cf.Antecedent(np.arange(0, 11, 1), 'conforto')
localidade = cf.Antecedent(np.arange(0, 11, 1), 'localidade')

estrelas = cf.Consequent(np.arange(0, 6, 1), 'estrelas')

# Definição das funções de pertinência
organizacao['ruim'] = fz.trimf(organizacao.universe, [0, 0, 5])
organizacao['aceitavel'] = fz.trimf(organizacao.universe, [0, 5, 10])
organizacao['boa'] = fz.trimf(organizacao.universe, [5, 10, 10])

atendimento['ruim'] = fz.trimf(atendimento.universe, [0, 0, 5])
atendimento['aceitavel'] = fz.trimf(atendimento.universe, [0, 5, 10])
atendimento['boa'] = fz.trimf(atendimento.universe, [5, 10, 10])

conforto['ruim'] = fz.trimf(conforto.universe, [0, 0, 5])
conforto['aceitavel'] = fz.trimf(conforto.universe, [0, 5, 10])
conforto['boa'] = fz.trimf(conforto.universe, [5, 10, 10])

localidade['ruim'] = fz.trimf(localidade.universe, [0, 0, 5])
localidade['aceitavel'] = fz.trimf(localidade.universe, [0, 5, 10])
localidade['boa'] = fz.trimf(localidade.universe, [5, 10, 10])

estrelas['pequena'] = fz.trimf(estrelas.universe, [0, 0, 2])
estrelas['media'] = fz.trimf(estrelas.universe, [1, 2.5, 4])
estrelas['alta'] = fz.trimf(estrelas.universe, [3, 5, 5])

# Visualização das funções de pertinência
organizacao.view()
atendimento.view()
conforto.view()
localidade.view()

estrelas.view()

# Definição das regras
r1 = cf.Rule(organizacao['ruim'] | atendimento['ruim'] | conforto['ruim'] | localidade['ruim'], estrelas['pequena'])
r2 = cf.Rule(organizacao['boa'] & atendimento['boa'] & conforto['boa'] & localidade['boa'], estrelas['alta'])
r3 = cf.Rule(organizacao['aceitavel'] & atendimento['aceitavel'] & conforto['aceitavel'] & localidade['aceitavel'], estrelas['media'])
r4 = cf.Rule(organizacao['ruim'] & atendimento['boa'] & conforto['boa'] & localidade['boa'], estrelas['media'])
r5 = cf.Rule(organizacao['aceitavel'] & atendimento['boa'] & conforto['aceitavel'] & localidade['boa'], estrelas['alta'])
r6 = cf.Rule(organizacao['boa'] & atendimento['aceitavel'] & conforto['boa'] & localidade['aceitavel'], estrelas['alta'])


# Processo de Inferência
criterios = cf.ControlSystem([r1, r2, r3, r4, r5, r6])
resultado = cf.ControlSystemSimulation(criterios)

resultado.input['organizacao'] = 6.5
resultado.input['atendimento'] = 8.0
resultado.input['conforto'] = 6.5
resultado.input['localidade'] = 9.0

# Processamento fuzzy e defuzzificação
resultado.compute()

# Saída
print("Valor de saída defuzzificado =", resultado.output['estrelas'])
y = resultado.output['estrelas']
print("Sugerindo um número de estrelas de %2.2f%%" % y)

# Visualização da saída
estrelas.view(sim=resultado)

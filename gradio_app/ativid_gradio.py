# draft1

import gradio as gr
import pandas as pd

import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]


ler_csv = lambda: pd.read_csv( ARQUIVO_CSV ).tail( 5 )

def cadastrar_paciente( nome, idade, convenio, prioridade, motivo ):

    linha = {
        "timestamp"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome":nome,  "idade":idade,  "convenio":convenio,  "prioridade":prioridade,  "motivo":motivo
    }

    exists = os.path.exists( ARQUIVO_CSV ) 

    novo   = pd.DataFrame( [linha] )
    novo.to_csv( ARQUIVO_CSV, mode= 'wa'[ exists ], header=not exists, index = False )

    return "Paciente cadastrado com sucesso!", ler_csv()

#end def

with gr.Blocks( title="Sistema de Cadastro de Pacientes", theme = gr.themes.Soft() ) as demo:

    gr.Markdown( "## Cadastro de Pacientes" )

    nome       = gr.Textbox  ( label  = "Nome do paciente" )
    idade      = gr.Number   ( label  = "Idade" )
    convenio   = gr.Dropdown ( label  = "Convênio",                         choices = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"] )
    prioridade = gr.Slider   ( label  = "Prioridade do atendimento",        minimum = 1, maximum = 5, step=1 )
    motivo     = gr.Textbox  ( label  = "Motivo da consulta / observações", lines = 3 )
     ##
    botao      = gr.Button   (  value = "Cadastrar" )
    sair       = gr.Button   (  value = "[encerra o servidor (durante testes) ]" )
    saida_msg  = gr.Textbox  ( label  = "Status",                           interactive = False)
    tabela     = gr.Dataframe( label  = "Últimos pacientes cadastrados",    value = ler_csv() )

    gr.update( tabela, pd.read_csv( ARQUIVO_CSV ).tail( 5 ) )

    pd.read_csv( ARQUIVO_CSV ).tail( 5 )

    botao.click( cadastrar_paciente,
                 [nome, idade, convenio, prioridade, motivo],
                 [saida_msg, tabela]    )
    sair.click ( lambda: demo.close() )
    
#end with    
    
demo.launch()
    

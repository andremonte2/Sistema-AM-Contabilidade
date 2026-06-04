# Controle de MEI
import streamlit as st
import datetime as dt
import pandas as pd
import os
import zipfile
from faturamento import faturamento1
from faturamento import notas_André

login = {
        "André": "2603",
        "Geraldo Assis": "1234"
         }

nome_empresarial = {
        "André": "12.345.678 André Monte",
        "Geraldo Assis": "67.000.097 GERALDO DE OLIVEIRA ASSIS"
        }

cnpj = {
        "André": "12.345.678/0001-23",
        "Geraldo Assis": "67.000.097/0001-03"
        }


meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

entrada = {"Geraldo Assis": "Junho"}

DAS = {
       "Janeiro":["André"],
       "Fevereiro":["André"],
       "Março":[""],
       "Abril":[""],
       "Maio":[""],
       "Junho":[""],
       "Julho":[""],
       "Agosto":[""],
       "Setembro":[""],
       "Outubro":[""],
       "Novembro":[""],
       "Dezembro":[""]
       }


mes_atual = dt.datetime.now().month
dia_atual = dt.datetime.now().day


st.title("AM Contabilidade")
st.subheader("Faça seu Login")
nome = st.text_input("Digite o seu nome de login!")

if nome in login:
    senha = st.text_input("Digite a sua senha de login!")
    if senha == login[nome]: 
        st.success("Você entrou no sistema da AM Contabilidade.")
        st.header(f"Bem-vindo ao sistema de gerenciamento MEI, {nome}!")
        st.subheader("Escolha o que quiser:")

        def controle_DAS():
            st.title("Controle de pagamento do DAS")
            st.divider(width="stretch")
            for mes in meses:

                indice = meses.index(mes)

                status = "DAS pago" if nome in DAS[mes] else f"Vencimento dia 20/{meses.index(mes)+2}/2026"
                status2 = "Pagamento realizado" if nome in DAS[mes] else "Não disponivel para pagamento"
                stt = "Não Conta" if indice < meses.index(entrada[nome]) else status4
                status3 = "Disponivel para pagamento" if mes_atual >= indice+2 else status2
                status4 = "Pagamento em atraso" if mes_atual == indice+2 and dia_atual > 20 or mes_atual > indice+2  else status3

                

                if indice == 11 and status != "DAS pago":
                    status = "Vencimento dia 20/01/2027"
                st.subheader(f"{mes}/2026: {status}")
                if stt == "Não Conta":
                    st.badge(stt,color=("gray"))
                else:
                    if status2 == "Pagamento realizado":
                        st.badge(status2,color=("green"))
                    elif status4 == "Pagamento em atraso":
                        st.markdown(":yellow-badge[Disponivel para pagamento] :red-badge[Pagamento em atraso]")
                    elif status3 == "Disponivel para pagamento":
                        st.badge(status3,color=("yellow"))
                    elif status2 == "Não disponivel para pagamento":
                        st.badge(status2,color=("blue"))
                
                if stt == "Não Conta":
                    st.markdown("")
                
                elif status == "DAS pago":
                    with open(f"AM Contabilidade/{nome}/Comprovantes/Comprovante_DAS_{mes}_2026.pdf","rb") as file:
                        st.download_button(
                            f"Baixar comprovante de pagamento do DAS de {mes}",
                            file,
                            file_name = f"Comprovante_DAS_{mes}_2026.pdf",
                            mime = "application/pdf"
                        )
                elif status3 == "Disponivel para pagamento":
                    with open(f"AM Contabilidade/{nome}/DAS/DAS_{mes}_2026.pdf","rb") as file:
                        st.download_button(
                            f"Baixar DAS {mes}",
                            file,
                            file_name = f"DAS_{mes}_2026.pdf",
                            mime = "application/pdf"
                        )
                else:
                    st.markdown("")
                st.divider()

        def dashboard():
            st.title("Dashboard")
            st.divider()
            st.subheader(f"Nome empresarial: {nome_empresarial[nome]}")
            st.subheader(f"CNPJ: {cnpj[nome]}")
            with open(f"AM Contabilidade/{nome}/Documentos/Cartão CNPJ.pdf","rb") as file:
                        st.download_button(
                            f"Baixar Cartão CNPJ",
                            file,
                            file_name = f"Cartão CNPJ - {nome_empresarial[nome]}.pdf",
                            mime = "application/pdf",
                        )
            st.divider()
            st.subheader("Status MEI: Regular✅")
            if dia_atual <= 20:
                proximo_mes = mes_atual
            else:
                proximo_mes = mes_atual+1
            
            if proximo_mes > 12:
                proximo_mes = 1
            st.subheader(f"Vencimento do Próximo DAS: 20/{proximo_mes:02d}/2026")
            
            das_pagos = 0
            for mes in meses:
                if nome in DAS[mes]:
                    das_pagos += 1
            st.subheader(f"DAS pagos em 2026: {das_pagos}/12")

            pendencias = 0
            for mes in meses:
                indice = meses.index(mes)
                status = 1 if mes_atual >= indice+2 and nome not in DAS[mes] and indice >=meses.index(entrada[nome]) else 2
                if status == 1:
                    pendencias += 1
            if pendencias > 0:
                st.subheader(f"Pendências: {pendencias} guias disponíveis para pagamento!")
            else:
                st.subheader(f"Nada consta como pendente, está em dia!")

            receita_total1 = 0
            for i in range(len(faturamento1[nome])):

                receita_total1 += faturamento1[nome][i]
            receita_total = "R$ {:,.2f}".format(receita_total1)
            media_atual1 = receita_total1 / len(faturamento1[nome])
            media_atual = "R$ {:,.2f}".format(media_atual1)
            st.subheader(f"Receita total de 2026: {receita_total}")
            st.subheader(f"Receita média por mês: {media_atual}")

        
        def Controle_Faturamento():
            st.title("Controle de Faturamento")
            st.divider()
            opcao = st.selectbox("Escolha a sessão que deseja:",("Receita de Vendas", "Notas Fiscais"),
                index=None,
                placeholder="Selecione um opção",
                key="periodo_faturamento",
            )

            receita_total1 = 0
            for i in range(len(faturamento1[nome])):

                receita_total1 += faturamento1[nome][i]
            receita_total = "R$ {:,.2f}".format(receita_total1)
            

            if opcao == "Receita de Vendas":
                st.subheader(f"Receita anual: {receita_total}")
                st.markdown("Meses com faturamento:")

                
                df = pd.DataFrame(
                         {
                             "Mês": meses[:len(faturamento1[nome])],
                              "Receita": faturamento1[nome]
                         }
                                    )
                df["Receita"] = df["Receita"].apply(lambda x: f"R$ {x:,.2f}")
                st.dataframe(df,hide_index=True)
            
                media_atual1 = receita_total1 / len(faturamento1[nome])
                media_atual = "R$ {:,.2f}".format(media_atual1)
                projecao1 = media_atual1 * 12
                projecao = "R$ {:,.2f}".format(projecao1)

                st.subheader(f"Faturamento médio por mês: {media_atual}")
                st.markdown(f"Projeção de Faturamento anual: {projecao}")
                st.markdown(f"Limite do faturamento anual MEI: R$81,000.00")
                if projecao1 > 81000:
                    st.badge("Chance de ultrapassar o limite do MEI", color="red")
                elif projecao1 > 70000:
                    st.badge("Cuidado para não ultrapassar o limite do MEI", color="yellow")
                elif projecao1 < 70000:
                    st.badge("Dentro do limite do MEI", color="green")
                
            if opcao == "Notas Fiscais":
                st.subheader("Deseja extrair as notas fiscais de qual periodo:")
                for mes in meses:
                    
                    pasta = (f"AM Contabilidade/{nome}/NFS_{mes}_2026")
                    def criar_zip(pasta, nome_zip):

                        with zipfile.ZipFile(
                            nome_zip,
                             "w",
                            zipfile.ZIP_DEFLATED
                        ) as zipf:

                            for raiz, dirs, arquivos in os.walk(pasta):

                                for arquivo in arquivos:

                                    caminho = os.path.join(
                                        raiz,
                                        arquivo
                                    )

                                    zipf.write(
                                        caminho,
                                        os.path.relpath(
                                            caminho,
                                            pasta
                                        )
                                    )
                    zip_nome = f"NFS_{mes}_2026.zip"

                    criar_zip(pasta,zip_nome)

                    if os.path.exists(pasta):
                        quantidade = len([

                        arquivo

                        for arquivo in os.listdir(pasta)

                        if os.path.isfile(
                            os.path.join(
                                pasta,
                                arquivo
                            )
                        )

                        ])
                    
                        st.subheader(f"{mes}/2026: ")
                        st.markdown(f"Quantidade total de Notas Fiscais: {quantidade}")
                        with open(
                        zip_nome,
                        "rb"
                        ) as arquivo:

                            st.download_button(

                                f"NFS_{mes}_2026",

                                arquivo,

                                file_name=
                                f"{zip_nome}",

                                mime=
                                "application/zip"
                            )
                    else:
                        st.subheader(f"{mes}/2026: ")
                        st.markdown(f"Quantidade total de Notas Fiscais: 0")
                

            
            
        if "pagina" not in st.session_state:
            st.session_state.pagina = "Dashboard"

        left,middle,right = st.columns(3)
        if left.button("Dashboard",type="primary",width="stretch"):
            st.session_state.pagina = "Dashboard"
            
        if middle.button("Controle de Pagamento DAS",type="primary",width="stretch"):
            st.session_state.pagina = "DAS"
            
        if right.button("Controle de Faturamento", type="primary",width="stretch"):
            st.session_state.pagina = "Faturamento"

        
        if st.session_state.pagina == "Dashboard":
            st.divider()
            dashboard()

        elif st.session_state.pagina == "DAS":
            st.divider()
            controle_DAS()

        elif st.session_state.pagina == "Faturamento":
            st.divider()
            Controle_Faturamento()
            

            
        
    elif senha =="":
        ""
    else:
        st.error("Senha Inválida!")
elif nome =="":
    ""
elif nome not in login:
    st.error("Nome Inválido!")



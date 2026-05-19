# Controle de MEI
import streamlit as st
import datetime as dt
import pandas as pd

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
login = {"André": "2603"}
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


st.title("AM Contabilidade")
st.header("Sistema de gerenciamento MEI")
st.subheader("Faça seu Login")
nome = st.text_input("Digite o seu nome de login!")

if nome in login:
    senha = st.text_input("Digite a sua senha de login!")
    if senha == login[nome]: 
        st.success("Você entrou no sistema da AM Contabilidade.")
        st.header(f"Bem-vindo ao sistema, {nome}!")
        st.title("Controle de pagamento do DAS")
        st.subheader("Vencimento da guia todo dia 20")
        st.divider(width="stretch")
        for mes in meses:

            indice = meses.index(mes)
            mes_atual = dt.datetime.now().month
            dia_atual = dt.datetime.now().day
    
            status = "DAS pago" if nome in DAS[mes] else f"Vencimento dia 20/{meses.index(mes)+2}/2026"
            status2 = "Pagamento realizado" if nome in DAS[mes] else "Não disponivel para pagamento"
            status3 = "Disponivel para pagamento" if mes_atual >= indice+2 else status2
            status4 = "Pagamento em atraso" if mes_atual == indice+2 and dia_atual > 20 or mes_atual > indice+2  else status3
            if indice == 11 and status != "DAS pago":
                status = "Vencimento dia 20/01/2027"
            st.subheader(f"{mes}/2026: {status}")
            if status2 == "Pagamento realizado":
                st.badge(status2,color=("green"))
            elif status4 == "Pagamento em atraso":
                st.markdown(":yellow-badge[Disponivel para pagamento] :red-badge[Pagamento em atraso]")
            elif status3 == "Disponivel para pagamento":
                st.badge(status3,color=("yellow"))
            elif status2 == "Não disponivel para pagamento":
                st.badge(status2,color=("red"))
            
            
            
            
            
            if status == "DAS pago":
                with open(f"C:\\Users\\andre\\Downloads\\AM Contabilidade\\Comprovante_DAS_{mes}_2026.pdf","rb") as file:
                    st.download_button(
                        f"Baixar comprovante de pagamento do DAS de {mes}",
                        file,
                        file_name = f"Comprovante_DAS_{mes}_2026.pdf",
                        mime = "application/pdf"
                    )
            elif status3 == "Disponivel para pagamento":
                with open(f"C:\\Users\\andre\\Downloads\\AM Contabilidade\\DAS_{mes}_2026.pdf","rb") as file:
                    st.download_button(
                        f"Baixar DAS {mes}",
                        file,
                        file_name = f"DAS_{mes}_2026.pdf",
                        mime = "application/pdf"
                    )
            else:
                st.markdown("")
            st.divider()
        
    else:
        st.error("Senha Inválida!")
if nome not in login:
    st.error("Nome Inválido!")



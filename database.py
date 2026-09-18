import streamlit as st
from datetime import datetime

from database import (
    criar_tabela,
    inserir_venda,
    listar_vendas,
    alterar_venda,
    excluir_venda
)


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Controle de Vendas",
    layout="wide"
)


# =========================================================
# CONFIGURAÇÃO ADMINISTRATIVA
# =========================================================

SENHA_ADMIN = st.secrets["SENHA_ADMIN"]


# =========================================================
# INICIALIZAÇÃO DO BANCO
# =========================================================

criar_tabela()


# =========================================================
# MENU LATERAL
# =========================================================

st.sidebar.title("Controle de Vendas")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "➕ Nova Venda",
        "📋 Vendas Realizadas"
    ]
)


# =========================================================
# PÁGINA: NOVA VENDA
# =========================================================

if pagina == "➕ Nova Venda":

    st.title("Nova Venda")

    st.write(
        "Registre uma nova encomenda de bolo."
    )

    # =====================================================
    # FORMULÁRIO DE CADASTRO
    # =====================================================

    with st.form("form_nova_venda"):

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # COLUNA ESQUERDA
        # -------------------------------------------------

        with col1:

            semana = st.number_input(
                "Semana",
                min_value=1,
                step=1
            )

            data_entrega = st.date_input(
                "Data de entrega",
                format="DD/MM/YYYY"
            )

            comprador = st.text_input(
                "Comprador"
            )

            valor = st.number_input(
                "Valor da venda",
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )

        # -------------------------------------------------
        # COLUNA DIREITA
        # -------------------------------------------------

        with col2:

            status_pagamento = st.selectbox(
                "Status do pagamento",
                [
                    "Pago",
                    "Pendente",
                    "Cortesia"
                ]
            )

            sabor = st.text_input(
                "Sabor"
            )

            pagador = st.text_input(
                "Pagador"
            )

        # -------------------------------------------------
        # BOTÃO REGISTRAR
        # -------------------------------------------------

        cadastrar = st.form_submit_button(
            "Registrar venda",
            type="primary"
        )

    # =====================================================
    # PROCESSAMENTO DO CADASTRO
    # =====================================================

    if cadastrar:

        if comprador.strip() == "":

            st.error(
                "Informe o comprador."
            )

        elif sabor.strip() == "":

            st.error(
                "Informe o sabor."
            )

        else:

            inserir_venda(
                semana=semana,

                # Banco recebe a data em AAAA-MM-DD
                data_entrega=str(data_entrega),

                comprador=comprador.strip(),
                valor=valor,
                status_pagamento=status_pagamento,
                sabor=sabor.strip(),
                pagador=pagador.strip()
            )

            st.success(
                "Venda cadastrada com sucesso!"
            )


# =========================================================
# PÁGINA: VENDAS REALIZADAS
# =========================================================

elif pagina == "📋 Vendas Realizadas":

    st.title("📋 Registro de Vendas")

    st.write(
        "Consulte, altere ou exclua vendas registradas."
    )

    # =====================================================
    # CARREGA OS REGISTROS
    # =====================================================

    df_vendas = listar_vendas()

    # =====================================================
    # VERIFICA SE EXISTEM REGISTROS
    # =====================================================

    if df_vendas.empty:

        st.info(
            "Nenhuma venda foi cadastrada até o momento."
        )

    else:

        # =================================================
        # DATAFRAME PARA EXIBIÇÃO
        # =================================================

        df_exibicao = df_vendas.copy()

        # Converte:
        # 2026-09-17
        # para
        # 17/09/2026

        df_exibicao["data_entrega"] = (
            df_exibicao["data_entrega"]
            .apply(
                lambda data: datetime.strptime(
                    data,
                    "%Y-%m-%d"
                ).strftime("%d/%m/%Y")
            )
        )

        # =================================================
        # EXIBIÇÃO DA TABELA
        # =================================================

        st.dataframe(
            df_exibicao,
            use_container_width=True,
            hide_index=True,
            column_config={

                "id": "ID",

                "semana": "Semana",

                "data_entrega": "Data de Entrega",

                "comprador": "Comprador",

                "valor": st.column_config.NumberColumn(
                    "Valor",
                    format="R$ %.2f"
                ),

                "status_pagamento": "Pagamento",

                "sabor": "Sabor",

                "pagador": "Pagador"
            }
        )

        st.divider()

        # =================================================
        # GERENCIAMENTO
        # =================================================

        st.subheader("⚙️ Gerenciar Venda")

        id_venda = st.selectbox(
            "Selecione o ID da venda:",
            df_vendas["id"].tolist()
        )

        # =================================================
        # LOCALIZA A VENDA SELECIONADA
        # =================================================

        venda = df_vendas[
            df_vendas["id"] == id_venda
        ].iloc[0]

        # =================================================
        # ALTERAR REGISTRO
        # =================================================

        with st.expander(
            "✏️ Alterar registro",
            expanded=False
        ):

            with st.form("form_alterar_venda"):

                col1, col2 = st.columns(2)

                # -----------------------------------------
                # COLUNA ESQUERDA
                # -----------------------------------------

                with col1:

                    nova_semana = st.number_input(
                        "Semana",
                        min_value=1,
                        value=int(venda["semana"]),
                        step=1
                    )

                    # Data armazenada no banco:
                    # AAAA-MM-DD

                    data_atual = datetime.strptime(
                        venda["data_entrega"],
                        "%Y-%m-%d"
                    ).date()

                    # Data exibida na tela:
                    # DD/MM/AAAA

                    nova_data = st.date_input(
                        "Data de entrega",
                        value=data_atual,
                        format="DD/MM/YYYY"
                    )

                    novo_comprador = st.text_input(
                        "Comprador",
                        value=venda["comprador"]
                    )

                    novo_valor = st.number_input(
                        "Valor",
                        min_value=0.0,
                        value=float(venda["valor"]),
                        step=1.0,
                        format="%.2f"
                    )

                # -----------------------------------------
                # COLUNA DIREITA
                # -----------------------------------------

                with col2:

                    status_opcoes = [
                        "Pago",
                        "Pendente",
                        "Cortesia"
                    ]

                    status_atual = venda[
                        "status_pagamento"
                    ]

                    if status_atual in status_opcoes:

                        indice_status = (
                            status_opcoes.index(
                                status_atual
                            )
                        )

                    else:

                        indice_status = 0

                    novo_status = st.selectbox(
                        "Status do pagamento",
                        status_opcoes,
                        index=indice_status
                    )

                    novo_sabor = st.text_input(
                        "Sabor",
                        value=venda["sabor"]
                    )

                    novo_pagador = st.text_input(
                        "Pagador",
                        value=venda["pagador"]
                    )

                # -----------------------------------------
                # SENHA ADMINISTRATIVA
                # -----------------------------------------

                st.divider()

                senha_alteracao = st.text_input(
                    "🔐 Senha administrativa",
                    type="password",
                    key="senha_alteracao"
                )

                salvar = st.form_submit_button(
                    "💾 Salvar alterações",
                    type="primary"
                )

            # =============================================
            # PROCESSAMENTO DO UPDATE
            # =============================================

            if salvar:

                if senha_alteracao != SENHA_ADMIN:

                    st.error(
                        "🔒 Senha administrativa incorreta."
                    )

                elif novo_comprador.strip() == "":

                    st.error(
                        "Informe o comprador."
                    )

                elif novo_sabor.strip() == "":

                    st.error(
                        "Informe o sabor."
                    )

                else:

                    alterar_venda(
                        id_venda=id_venda,
                        semana=nova_semana,

                        # Retorna ao banco em AAAA-MM-DD
                        data_entrega=str(nova_data),

                        comprador=novo_comprador.strip(),
                        valor=novo_valor,
                        status_pagamento=novo_status,
                        sabor=novo_sabor.strip(),
                        pagador=novo_pagador.strip()
                    )

                    st.success(
                        "Venda alterada com sucesso! ✅"
                    )

                    st.rerun()

        # =================================================
        # EXCLUIR REGISTRO
        # =================================================

        with st.expander(
            "🗑️ Excluir registro",
            expanded=False
        ):

            st.warning(
                f"Você está prestes a excluir "
                f"permanentemente a venda ID {id_venda}."
            )

            # ---------------------------------------------
            # SENHA
            # ---------------------------------------------

            senha_exclusao = st.text_input(
                "🔐 Senha administrativa",
                type="password",
                key="senha_exclusao"
            )

            # ---------------------------------------------
            # CONFIRMAÇÃO
            # ---------------------------------------------

            confirmar_exclusao = st.checkbox(
                "Confirmo que desejo excluir este registro."
            )

            # ---------------------------------------------
            # BOTÃO
            # ---------------------------------------------

            excluir = st.button(
                "🗑️ Excluir venda",
                type="primary",
                disabled=not confirmar_exclusao
            )

            # =============================================
            # PROCESSAMENTO DO DELETE
            # =============================================

            if excluir:

                if senha_exclusao != SENHA_ADMIN:

                    st.error(
                        "🔒 Senha administrativa incorreta."
                    )

                else:

                    excluir_venda(
                        id_venda
                    )

                    st.success(
                        "Registro excluído com sucesso!"
                    )

                    st.rerun()

#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════════
#  PyQuest — Instalación automática para Termux
#  Aprende Python como un héroe, directo en tu terminal
#
#  Uso:
#    pkg install git -y
#    git clone https://github.com/tu-usuario/pyquest.git
#    cd pyquest
#    bash setup_termux.sh
# ═══════════════════════════════════════════════════════════

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BOLD}${GREEN}  ╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}  ║     ${YELLOW}PyQuest — Instalación en Termux${GREEN}     ║${NC}"
echo -e "${BOLD}${GREEN}  ║  ${CYAN}Aprende Python como un héroe${GREEN}        ║${NC}"
echo -e "${BOLD}${GREEN}  ╚══════════════════════════════════════════╝${NC}"
echo ""

# ─── Detectar Termux ───
if [ -z "$TERMUX_VERSION" ]; then
    echo -e "${YELLOW}⚠  No se detecta Termux. Continuando igualmente...${NC}"
fi

# ─── 1. Actualizar paquetes ───
echo -e "${CYAN}📦 Actualizando repositorios...${NC}"
pkg update -y -qq 2>/dev/null || true

# ─── 2. Instalar dependencias ───
echo -e "${CYAN}📦 Instalando Python y dependencias...${NC}"
pkg install -y python python-pip git 2>/dev/null || {
    echo -e "${RED}Error instalando paquetes. ¿Estás en Termux?${NC}"
    exit 1
}

# ─── 3. Instalar dependencias Python ───
echo -e "${CYAN}🐍 Instalando librerías Python...${NC}"
pip install rich prompt-toolkit 2>/dev/null || pip3 install rich prompt-toolkit 2>/dev/null || {
    echo -e "${YELLOW}⚠  Instalando sin pip... intentando con apt${NC}"
    pkg install -y python-rich 2>/dev/null || true
}

# ─── 4. Verificar instalación ───
echo ""
echo -e "${CYAN}🔍 Verificando instalación...${NC}"

if python3 -c "import rich" 2>/dev/null; then
    echo -e "  ${GREEN}✓ rich — OK${NC}"
else
    echo -e "  ${RED}✗ rich — NO INSTALADO${NC}"
    echo -e "  ${YELLOW}  Ejecuta: pip install rich${NC}"
fi

if python3 -c "import prompt_toolkit" 2>/dev/null; then
    echo -e "  ${GREEN}✓ prompt-toolkit — OK${NC}"
else
    echo -e "  ${RED}✗ prompt-toolkit — NO INSTALADO${NC}"
    echo -e "  ${YELLOW}  Ejecuta: pip install prompt-toolkit${NC}"
fi

# ─── 5. Alias para fácil acceso ───
if ! grep -q "alias pyquest" ~/.bashrc 2>/dev/null; then
    echo -e "${CYAN}🔗 Agregando alias 'pyquest' a ~/.bashrc...${NC}"
    echo "" >> ~/.bashrc
    echo "# PyQuest - Terminal RPG para aprender Python" >> ~/.bashrc
    echo "alias pyquest='cd ${PWD} && python3 main.py'" >> ~/.bashrc
    echo "alias pyquest-docs='cd ${PWD} && python3 main.py --docs'" >> ~/.bashrc
    echo "alias pyquest-play='cd ${PWD} && python3 main.py --playground'" >> ~/.bashrc
fi

# ─── 6. Limpiar y finalizar ───
echo ""
echo -e "${BOLD}${GREEN}  ──────────────────────────────────────────${NC}"
echo -e "${BOLD}${GREEN}  ✅  PyQuest instalado correctamente${NC}"
echo -e "${BOLD}${GREEN}  ──────────────────────────────────────────${NC}"
echo ""
echo -e "  ${CYAN}Para jugar:${NC}"
echo -e "    ${BOLD}python main.py${NC}"
echo -e "    ${BOLD}pyquest${NC}          (después de reiniciar Termux)"
echo ""
echo -e "  ${CYAN}Documentación interactiva:${NC}"
echo -e "    ${BOLD}python main.py --docs${NC}"
echo -e "    ${BOLD}/docs${NC}            (dentro del juego)"
echo ""
echo -e "  ${CYAN}Playground (REPL libre):${NC}"
echo -e "    ${BOLD}python main.py --playground${NC}"
echo -e "    ${BOLD}/playground${NC}      (dentro del juego)"
echo ""
echo -e "  ${CYAN}Actualizar zonas:${NC}"
echo -e "    ${BOLD}git pull${NC}"
echo -e "    ${BOLD}/git pull${NC}        (dentro del juego)"
echo ""
echo -e "  ${CYAN}Comandos dentro del juego:${NC}"
echo -e "    ${BOLD}/docs${NC}       Documentación interactiva de Python"
echo -e "    ${BOLD}/docs buscar <q>${NC}  Buscar en la documentación"
echo -e "    ${BOLD}/playground${NC} REPL libre para experimentar"
echo -e "    ${BOLD}/mapa${NC}       Ver mapa de zonas"
echo -e "    ${BOLD}/perfil${NC}     Ver estadísticas y progreso"
echo -e "    ${BOLD}/git pull${NC}   Actualizar desde Git"
echo -e "    ${BOLD}/ayuda${NC}      Mostrar comandos disponibles"
echo ""
echo -e "  ${YELLOW}🎮  ¡A programar, dev!${NC}"
echo ""

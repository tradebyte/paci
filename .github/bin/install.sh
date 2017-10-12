#!/usr/bin/env bash
#
# Description: This script installs the paci package manager.
# Author: Niklas Heer (niklas.heer@tradebyte.com)
# Version: 1.0.0 (2017-10-12)

print_success() {
    echo "${GREEN}"
    echo "                   __ "
    echo ".-----.---.-.----.|__|"
    echo "|  _  |  _  |  __||  |"
    echo "|   __|___._|____||__|"
    echo "|__|                  ....is now ${BOLD}installed!${NORMAL}"
    echo ""
    echo ""
    echo "For more information about this tool, visit our Github repository:"
    echo "https://github.com/tradebyte/paci"
    echo ""
}

determine_os() {
    # Determine OS platform
    export DISTRO

    UNAME=$(uname | tr "[:upper:]" "[:lower:]")
    # If Linux, try to determine specific distribution
    if [ "$UNAME" == "linux" ]; then
        # If available, use LSB to identify distribution
        if [ -f /etc/lsb-release ] || [ -d /etc/lsb-release.d ]; then
            DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)
            # Otherwise, use release info file
        else
            # shellcheck disable=SC2010
            DISTRO=$(ls -d /etc/[A-Za-z]*[_-][rv]e[lr]* | grep -v "lsb" | cut -d'/' -f3 | cut -d'-' -f1 | cut -d'_' -f1)
        fi
    fi
    # For everything else (or if above failed), just use generic identifier
    [ "$DISTRO" == "" ] && DISTRO=$UNAME
    unset UNAME
}

check_dependencies() {
    # Gether information about installed and missing packages
    for pkg in $1; do
        if [ $(dpkg-query -W -f='${Status}' $pkg 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
            missing_pkgs+=($pkg)
        else
            installed_pkgs+=($pkg)
        fi
    done

    # Display installed packages
    if [ ${#installed_pkgs[@]} -ge 1 ]; then
        versions=$(dpkg-query -W -f='[ok] ${Package}: ${Version}\n' ${installed_pkgs[@]})
        installed="${versions//\[ok\]/  $OK}"
        echo -e "$installed"
    fi

    # Display and handle missing packages
    if [ ${#missing_pkgs[@]} -eq 0 ]; then
        # OK
        echo -e "\n  ${RETURN}${GREEN} All dependencies are installed. ${BOLD}Everything ok!${NORMAL} "
    else
        # Display missing packages
        for pkg in ${missing_pkgs[@]}; do
            echo "  ${ERR} $pkg"
        done

        # Install missing packages
        echo -e "\n${RETURN}${YELLOW} Installing missing packages...${NORMAL}"
        (sudo apt-get -y install ${missing_pkgs[@]} >/dev/null 2>&1)
        if [ $? -eq 0 ]; then
            echo -e "  ${OK} All dependencies are now installed."
        else
            echo -e "\n${ERR} Failed to install dependencies. Abort."
        fi
    fi
}

main() {
    # Use colors, but only if connected to a terminal, and that terminal
    # supports them.
    if which tput >/dev/null 2>&1; then
        ncolors=$(tput colors)
    fi
    if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
        RED="$(tput setaf 1)"
        GREEN="$(tput setaf 2)"
        YELLOW="$(tput setaf 3)"
        BLUE="$(tput setaf 4)"
        BOLD="$(tput bold)"
        LINE="$(tput smul)"
        NORMAL="$(tput sgr0)"
    else
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        BOLD=""
        NORMAL=""
    fi

    OK=$(printf "${GREEN}${BOLD}\xE2\x9C\x94${NORMAL}")
    ERR=$(printf "${RED}${BOLD}\xE2\x9C\x97${NORMAL}")
    INFO=$(printf "${BLUE}${BOLD}\xE2\x97\x8F${NORMAL}")
    RETURN=$(printf "${BLUE}${BOLD}\xE2\x86\xAA${NORMAL}")

    # Only enable exit-on-error after the non-critical colorization stuff,
    # which may fail on systems lacking tput or terminfo
    set -e

    echo -e "${GREEN}${BOLD}Welcome to the paci installer.\n\n"

    # TODO:
    # 0. Check System (Ubuntu)
    # 1. Check requirements
    # 2. Install via pip
    # 3. Ensure paci is in $PATH
    # 4. Setup (inkl. input param -> main/fallback)

    # Step 0: Determine if we have a compatible OS
    determine_os

    if [ "$DISTRO" == "Ubuntu" ] || [ "$DISTRO" == "Debian" ]; then
        # Step 1: Check or install the requirements
        echo "${INFO}${YELLOW} Checking dependencies...${NORMAL}"
        check_dependencies "python3 python3-venv python3-pip rsync fish"

        # Step 2: Install via pip
        echo -e "\n${INFO}${YELLOW} Installing paci via pip...${NORMAL}"
        (pip3 install --upgrade paci >/dev/null 2>&1)
        if [ $? -eq 0 ]; then
            echo -e "  ${OK} Installation successful."
        else
            echo -e "\n${ERR} Failed installation. Abort."
        fi

        # Step 3: Verify $PATH
        echo -e "\n${INFO}${YELLOW} Verifing \$PATH...${NORMAL}"

        # Write a message in case the $PATH doesn't contain the command
        bail() {
            failed=1
            echo -e "  ${ERR} The ${BOLD}paci${NORMAL} command is not in your \$PATH!"
            echo -e "    Please add ${BLUE}export PATH=\"\$PATH:\$HOME/.local/bin\"${NORMAL} to your ${BLUE}~/.bashrc${NORMAL}!"
        }

        # Test if the command exsits
        command -v paci >/dev/null 2>&1 || bail

        # Everything OK
        if [ -v $failed ]; then
            echo -e "  ${OK}${GREEN} The ${LINE}\$PATH${NORMAL}${GREEN} is set. ${BOLD}Everything ok!${NORMAL}"
        fi
    else
        echo "${ERR}${RED} You are running this script on an unsupported OS!${NORMAL}"
        echo ""
        echo "At the moment we only support:"
        echo " - Ubuntu"
        echo " - Debian"
        exit
    fi

    print_success
}

main "$@"

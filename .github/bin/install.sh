#!/usr/bin/env bash
#
# Description: This script installs the paci package manager.
# Author: Niklas Heer (niklas.heer@tradebyte.com)
# Version: 1.1.0 (2017-10-13)

spinner() {
    local pid=$1
    local delay=0.3
    # shellcheck disable=SC1003
    local spinstr='|/-\'
    while ps a | awk '{print $1}' | grep -q "$pid"; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
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
        # shellcheck disable=SC2016
        if [ "$(dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -c 'ok installed')" -eq 0 ]; then
            missing_pkgs+=($pkg)
        else
            installed_pkgs+=($pkg)
        fi
    done

    # Display installed packages
    if [ ${#installed_pkgs[@]} -ge 1 ]; then
        # shellcheck disable=SC2016
        versions="$(dpkg-query -W -f='[ok] ${Package}: ${Version}\n' "${installed_pkgs[@]}")"
        installed="${versions//\[ok\]/  $OK}"
        echo -e "$installed"
    fi

    # Display and handle missing packages
    if [ ${#missing_pkgs[@]} -eq 0 ]; then
        # OK
        echo -e "\n  ${RETURN}${GREEN} All dependencies are installed. ${BOLD}Everything ok!${NORMAL} "
    else
        # Display missing packages
        for pkg in "${missing_pkgs[@]}"; do
            echo "  ${ERR} $pkg"
        done

        # Install missing packages
        printf "\n%s Installing missing packages...${NORMAL}" "${RETURN}${YELLOW}"
        (sudo apt-get -y install "${missing_pkgs[@]}" >/dev/null 2>&1) &
        spinner $!
        if [ $? -eq 0 ]; then
            echo -e "\n  ${OK} All dependencies are now installed."
        else
            echo -e "\n  ${ERR} Failed to install dependencies. Abort."
        fi
    fi
}

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

run_configuration() {
    cmd_configure=$1

    # Ask if they want to use the defaults
    read -p "  ${RETURN} Do you want to use the defaults (Y/n)? " yn
    case $yn in
        [Nn]) echo "" ;;
        *)
            cmd_configure+=("--no-choice")
            cmd_configure+=("--silent")
            ;;
    esac

    # Use if set the main registry
    if [ ! -z "$MAIN_URL" ]; then
        cmd_configure+=("--main-registry=$MAIN_URL")
    fi

    # Use if set the fallback registry
    if [ ! -z "$FALLBACK_URL" ]; then
        cmd_configure+=("--fallback-registry=$FALLBACK_URL")
    fi

    # Actually run the paci configure command
    "${cmd_configure[@]}"

    echo -e "  ${OK} Configuration successful."
}

main() {
    # Save parameters for later use
    MAIN_URL="$1"
    FALLBACK_URL="$2"

    # Define settings
    REQs="python3 python3-venv python3-pip rsync git jq"
    PY_REQs=("paci" "halo" "termcolor" "easydict" "log_symbols" "tldr")

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
        NORMAL="$(tput sgr0)"
        LINE="$(tput smul)"

        OK=$(printf "%s\xE2\x9C\x94${NORMAL}" "${GREEN}${BOLD}")
        ERR=$(printf "%s\xE2\x9C\x97${NORMAL}" "${RED}${BOLD}")
        INFO=$(printf "%s\xE2\x9D\x90${NORMAL}" "${BLUE}${BOLD}")
        INPUT=$(printf "%s\xE2\x9D\x93${NORMAL}" "${RED}${BOLD}")
        RETURN=$(printf "%s\xE2\x86\xAA${NORMAL}" "${BLUE}${BOLD}")
    else
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        BOLD=""
        NORMAL=""
        LINE=""

        # Fallback symbols
        OK=$(printf "[ok]")
        ERR=$(printf "[error]")
        INFO=$(printf "[info]")
        INPUT=$(printf "[?]")
        RETURN=""
    fi

    # Let's start
    echo -e "${GREEN}${BOLD}Welcome to the paci installer.\n\n"

    # Step 0: Determine if we have a compatible OS or if we want to skip
    # Ask if they want to skip the check
    read -p "  ${INPUT}${YELLOW} Do you want to skip the compatibility check (y/N)? " yn
    case $yn in
        [Yy]) SKIP="true" ;;
        *)
            determine_os
            echo ""
            ;;
    esac
    echo ""

    if [ "$DISTRO" == "Ubuntu" ] || [ "$DISTRO" == "Debian" ] || [ "$SKIP" == "true" ] ; then
        # Step 1: Check or install the requirements
        echo "${INFO}${YELLOW} Checking dependencies...${NORMAL}"
        check_dependencies "$REQs"

        # Step 2: Install via pip
        printf "\n%s Installing paci via pip...${NORMAL}" "${INFO}${YELLOW}"
        (pip3 install --user --upgrade "${PY_REQs[@]}" >/dev/null 2>&1) &
        spinner $!
        if [ $? -eq 0 ]; then
            echo -e "\n  ${OK} Installation successful."
        else
            echo -e "\n  ${ERR} Failed installation. Abort."
        fi

        # Step 3: Verify $PATH
        echo -e "\n${INFO}${YELLOW} Verifying \$PATH...${NORMAL}"

        # Write a message in case the $PATH doesn't contain the command
        bail() {
            failed=1
            echo -e "  ${ERR} The ${BOLD}paci${NORMAL} command is not in your \$PATH!"
            echo -e "    Please add ${BLUE}export PATH=\"\$PATH:\$HOME/.local/bin\"${NORMAL} to your ${BLUE}~/.bashrc${NORMAL} or ${BLUE}~/.zshrc${NORMAL}!\n"
            export PATH="$PATH:$HOME/.local/bin"
            echo -e "    The ${LINE}\$PATH${NORMAL} variable was temporarily set."
        }

        # Test if the command exsits
        command -v paci >/dev/null 2>&1 || bail

        # Everything OK
        if [ -v $failed ]; then
            echo -e "  ${OK}${GREEN} The ${LINE}\$PATH${NORMAL}${GREEN} is set. ${BOLD}Everything ok!${NORMAL}"
        fi

        # Step 4: Configure paci
        echo -e "\n${INFO}${YELLOW} Configuring paci...${NORMAL}"
        cmd_configure=(paci)
        cmd_configure+=("configure")
        if [ ! -f "$HOME/.config/paci/settings.yml" ]; then
            run_configuration "${cmd_configure[@]}"
        else

            echo -e "  ${RETURN}${GREEN} Configuration already present.${NORMAL}\n"

            # Ask if they want to overwrite it
            read -p "  ${INPUT}${YELLOW} Do you want to overwrite the config (y/N)? " yn
            case $yn in
                [Yy]) run_configuration "${cmd_configure[@]}" ;;
                *)
                    echo ""
                    ;;
            esac
        fi

        # Step 5: Refresh paci registries
        printf "\n%s Refreshing paci index...${NORMAL}" "${INFO}${YELLOW}"
        (paci refresh >/dev/null 2>&1) &
        spinner $!
        if [ $? -eq 0 ]; then
            echo -e "\n  ${OK} Everything up to date!"
        else
            echo -e "\n  ${ERR} Failed to update. Abort."
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

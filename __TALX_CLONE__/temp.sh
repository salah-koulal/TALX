# push function
/mnt/c/Users/Active/AppData/Local/Temp
function push1() {
    local commit_message="$(date)"
    local branch=""
    local create_branch=false
    local commit_all=false

    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            -c)
            shift
            if [[ -n "$1" ]]; then
                commit_message="$1"
                shift
            fi
            ;;
            -b)
            shift
            if [[ -n "$1" ]]; then
                branch="$1"
                shift
            fi
            ;;
            -cb)
            shift
            if [[ -n "$1" ]]; then
                branch="$1"
                create_branch=true
                shift
            fi
            ;;
            -ca)
            shift
            commit_all=true
            if [[ -n "$1" ]]; then
                commit_message="$1"
                shift
            fi
            ;;
            *)
            shift
            ;;
        esac
    done

    if $create_branch; then
        git checkout -b "$branch"
    elif [[ -n "$branch" ]]; then
        git checkout "$branch"
    fi

    if $commit_all; then
        git add .
        git commit -a -m "$commit_message"
    else
        git add .
        git commit -m "$commit_message"
    fi

    if [[ -n "$branch" ]]; then
        git push origin "$branch"
    else
        git push
    fi
}

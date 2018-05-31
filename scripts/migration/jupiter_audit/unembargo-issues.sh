while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"

    curl "$line" >> "unembargo.txt"
done < "unembargo-issues.txt"
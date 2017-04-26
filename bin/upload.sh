
complete_dir="/downloads/complete"

for entry in "$complete_dir"/*
do
    echo "$entry"
    echo "$entry"
    flock -n "$entry" -c "cd $complete_dir && drive upload -f '$entry' -p 0B6VJgbksxQNSNHRJSmRtS0ZWMXM  && rm -rf '$entry'"
    break
done



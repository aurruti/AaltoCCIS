# File 2dot4.awk
# Aitor Urruticoechea 2023

BEGIN{
    sum_a = 0
    sum_b = 0
    sum_c = 0
    sum_total = 0
}
NR>1 && length($7)!=0 && $7!=0{
sum_total += 1;
if ($10/$7 > 0.01)
    sum_a += 1;
    if ($10/$7 > 0.1)
        sum_b += 1;
        if ($10/$7 > 0.2)
            sum_c += 1;
}
END{
    print FILENAME
    print "PERCENTAGES"
    print (sum_a/sum_total)*100
    print (sum_b/sum_total)*100
    print (sum_c/sum_total)*100
}

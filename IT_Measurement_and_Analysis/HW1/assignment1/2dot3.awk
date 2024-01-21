# File 2dot3.awk
# Aitor Urruticoechea 2023

BEGIN{
    n_total=0
    sum_total=0
    sum_3 =0
    sum_7 =0
    sum_10 =0
    sum_17 =0
    sum_21 =0
    sum_24 =0
}
{sum_total = sum_total + $3 + $7 + $10 + $17 + $21 + $24}
{num_total= num_total+1}
{sum_3 = sum_3+ $3}
{sum_7 = sum_7+ $7}
{sum_10 = sum_10+ $10}
{sum_17 = sum_17+ $17}
{sum_21 = sum_21+ $21}
{sum_24 = sum_24+ $24}
END{
    print FILENAME
    print "AVERAGES"
    print sum_3/num_total    
    print sum_7/num_total
    print sum_10/num_total
    print sum_17/num_total
    print sum_21/num_total
    print sum_24/num_total
    print sum_total/(num_total*6)
}
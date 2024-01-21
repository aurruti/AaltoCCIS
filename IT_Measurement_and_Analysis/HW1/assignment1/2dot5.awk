# File 2dot5.awk
# Aitor Urruticoechea 2023

BEGIN{
    max3 = 0
    max9 = 0
    max17 = 0
    max23 = 0
    max31 = 0
}
NR!=1 {
if ($3 > max3)
    max3 = $3;
if ($9 > max9)
    max9 = $9;
if ($17 > max17)
    max17 = $17;
if ($23 > max23)
    max23 = $23;
if ($31 > max31)
    max31 = $31;
}
END{
    print FILENAME
    print "MAXIMUMS"
    print max3
    print max9
    print max17
    print max23
    print max31
}
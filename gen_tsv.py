import os
rows = []
rows.append("Input_X\tInput_Y\tPath\tSegCount\tCumSeg\tOutIdx\tSrcRow\tSegIdx\tt\tOutX\tOutY\tdX_Blend\tdY_Blend\tBaseZ_Deg\tZ_Deg_Offset\tGCODE\t\tSetting\tValue")
rows.append("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tZ_OFFSET_DEG\t0")
rows.append("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCURVE_SEGMENTS\t20")
rows.append("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t")

for r in range(5, 421):
    A, B, C = "", "", ""
    if r == 5: A, B = "0", "0"
    elif r == 6: A, B, C = "20", "0", "S"
    elif r == 7: A, B, C = "40", "20", "C"
    elif r == 8: A, B, C = "60", "20", "S"

    D = ""
    if r == 5: D = "0"
    elif r <= 120: D = "=IF(C{r}=\"C\",$S$3,IF(C{r}=\"S\",1,0))".format(r=r)

    E = ""
    if r == 5: E = "0"
    elif r <= 120: E = "=E{rm1}+D{r}".format(rm1=r-1, r=r)

    F = "=ROW()-4"
    G = "=IF(F{r}>LOOKUP(9.99999999999999E+307,$E$5:$E$120),\"\",LOOKUP(F{r}-1,$E$5:$E$120,ROW($E$5:$E$120))+1)".format(r=r)
    H = "=IF(G{r}=\"\",\"\",F{r}-INDEX($E:$E,G{r}-1))".format(r=r)
    I = "=IF(G{r}=\"\",\"\",H{r}/INDEX($D:$D,G{r}))".format(r=r)

    J_core = "IF(G{r}=\"\",\"\",IF(INDEX($C:$C,G{r})=\"C\",0.5*(2*(INDEX($A:$A,G{r}-1))+(-(INDEX($A:$A,MAX(5,G{r}-2)))+(INDEX($A:$A,G{r})))*I{r}+(2*(INDEX($A:$A,MAX(5,G{r}-2)))-5*(INDEX($A:$A,G{r}-1))+4*(INDEX($A:$A,G{r}))-(INDEX($A:$A,MIN(LOOKUP(2,1/((($A$5:$A$120<>\"\")+($B$5:$B$120<>\"\"))>0),ROW($A$5:$A$120)),G{r}+1))))*I{r}^2+(-(INDEX($A:$A,MAX(5,G{r}-2)))+3*(INDEX($A:$A,G{r}-1))-3*(INDEX($A:$A,G{r}))+(INDEX($A:$A,MIN(LOOKUP(2,1/((($A$5:$A$120<>\"\")+($B$5:$B$120<>\"\"))>0),ROW($A$5:$A$120)),G{r}+1))))*I{r}^3),INDEX($A:$A,G{r}-1)+(INDEX($A:$A,G{r})-INDEX($A:$A,G{r}-1))*I{r}))".format(r=r)
    J = "=" + J_core
    K_core = J_core.replace("$A:$A", "$B:$B")
    K = "=" + K_core

    L = "=IF(J{r}=\"\",\"\",IF(AND(J{rm1}<>\"\",J{rp1}<>\"\"),(J{rp1}-J{rm1})/2,IF(J{rp1}<>\"\",J{rp1}-J{r},IF(J{rm1}<>\"\",J{r}-J{rm1},\"\"))))".format(r=r, rm1=r-1, rp1=r+1)
    M = "=IF(K{r}=\"\",\"\",IF(AND(K{rm1}<>\"\",K{rp1}<>\"\"),(K{rp1}-K{rm1})/2,IF(K{rp1}<>\"\",K{rp1}-K{r},IF(K{rm1}<>\"\",K{r}-K{rm1},\"\"))))".format(r=r, rm1=r-1, rp1=r+1)
    N = "=IF(L{r}=\"\",\"\",MOD(DEGREES(ATAN2(L{r},M{r})),360))".format(r=r)
    O = "=IF(N{r}=\"\",\"\",N{r}+$S$2)".format(r=r)
    P = "=IF(O{r}=\"\",\"\",\"G1 X\"&TEXT(J{r},\"0.###\")&\" Y\"&TEXT(K{r},\"0.###\")&\" Z\"&TEXT(O{r},\"0.###\"))".format(r=r)

    # Note: Using R column for Setting and S for Value starting rows 2/3.
    # The columns are A:P and R:S. Q is blank (index 16).
    row_data = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, "", "", ""]
    # Adjusting Row 2 and 3 specifically in the loop after creation or inserting them first?
    # Actually I appended Row 1..4 first. The loop starts from r=5.

    rows.append("\t".join(row_data))

with open(r"docs/GCODE_G1_Continuous_Tangent_Blended_Generator_LO.tsv", "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\r\n".join(rows))


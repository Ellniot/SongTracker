from os import stat


def main2():
    sql_script_file = open("./sql/TopCountPastMonth.sql", 'r')
    sql_script = sql_script_file.read()
    print(sql_script)

    new_sql_script = sql_script%("jack_fm", 5, 22)
    print(new_sql_script)

def main():
    str1 = "helloasdf"
    print(str1.isnumeric())
    #print(int(str1))

main()
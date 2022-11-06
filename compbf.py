from string import printable
import sys

# FIXME: really weird bug when program ends in sN
def decompress(code):
    commands = ['+', '-', '<', '>', '.', ',', '[', ']']
    perms = [(x, y) for x in commands for y in commands] + [(x, y, z) for x in commands for y in commands for z in commands]
    perms = [''.join(list(t)) for t in perms]
    keys = [x for x in printable if not x in commands] + [chr(_) for _ in range(174,576+82)]
    
    dictf = {}
    for key, val in zip(keys, perms):
        dictf[key] = val
    
    new_code = ""
    skip_it = False
    for i, s in enumerate(code):
        if i == len(code)-1:
            new_code += dictf[s]
        elif skip_it:
            skip_it = False
            continue
        elif s in commands and code[i+1].isnumeric():
            new_code += ''.join([s for _ in range(int(code[i+1]))])
            skip_it = True
        elif s in commands:
            new_code += s
        elif s in dictf:
            new_code += dictf[s]
        else:
            continue

    return new_code

def evaluate(input):
    i = 0
    code = ''
    for e in input:
     code += ' ' * i + [
         'i+=1',
         'i-=1',
         'b[i]+=1',
         'b[i]-=1',
         'sys.stdout.write(chr(b[i]))',
         'b[i]=ord(sys.stdin.read(1))',
         'while b[i]:',
         'pass',
         ''
     ]['><+-.,['.find(e)]+'\n'
     i += (92 - ord(e)) * (e in '][')
    exec(f"i={i}\nb=[0]*30000\n"+code) 
    # print(f"i={i}\nb=[0]*30000\n"+code)

# FIXME: "+8P+4P&#o&{<ġŕ\rr6nġŮpÞ+7A#ƭƣƦ#.-6.-8ƭ4o4##" doesnt work in the cmd
def main():
    args = sys.argv[1:]
    if args[0] == 'e':
        evaluate(decompress(args[1]))
    else:
        with open(args[0], 'r', encoding='utf-8') as f:
            evaluate(decompress(f.read()))

if __name__ == '__main__':
    main()


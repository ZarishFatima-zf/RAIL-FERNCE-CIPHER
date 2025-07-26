from flask import Flask, render_template, request
app = Flask(__name__)

def print_box(matrix_fence):
    depth = len(matrix_fence)
    print("+" + "---+" * len(matrix_fence[0]))
    for row in range(depth):
        print("| " + " | ".join(matrix_fence[row]) + " |")
        print("+" + "---+" * len(matrix_fence[0]))

def rail_fence_cipher_encryption(text, depth):
    text = text.replace(" ", "")  
    matrix_fence= [[' '] * len(text) 
              for i in range(depth)]
    row = 0
    downward = True
    for col in range(len(text)):
        matrix_fence[row][col] = text[col]
        if downward:
            row += 1
        else:
            row -= 1
        # Change direction when reaching the top or bottom
        if row == depth:
            row = depth - 2
            downward = False
        elif row == -1:
            row = 1
            downward = True
            
    print_box(matrix_fence)
    encrypted_text = ""
    for r in range(depth):
        for c in range(len(text)):
            if matrix_fence[r][c] != ' ':
                encrypted_text += matrix_fence[r][c]
    return encrypted_text

def rail_fence_cipher_decryption(text, depth):
    # Create an empty matrix for the fence
    matrix_fence = [[''] * len(text) for i in range(depth)]
    row, downward = 0, True

    # First, mark the places in the matrix where characters will go
    for col in range(len(text)):
        matrix_fence[row][col] = '*'
        if downward:
            row += 1
        else:
            row -= 1
        if row == depth:
            row = depth - 2
            downward = False
        elif row == -1:
            row = 1
            downward = True

    # Fill the matrix with characters from the ciphertext
    idx = 0
    for r in range(depth):
        for c in range(len(text)):
            if matrix_fence[r][c] == '*':
                matrix_fence[r][c] = text[idx]
                idx += 1

    # Now, read the matrix in the zigzag order to get the decrypted text
    result = []
    row, downward = 0, True
    for col in range(len(text)):
        result.append(matrix_fence[row][col])
        if downward:
            row += 1
        else:
            row -= 1
        if row == depth:
            row = depth - 2
            downward = False
        elif row == -1:
            row = 1
            downward = True

    return ''.join(result)

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_message = decrypted_message = plain_text = depth = None
    if request.method == 'POST':
        message = request.form['message']
        depth = int(request.form.get('key_index'))
        action = request.form['action']
        plain_text = message
        if action == 'Encrypt':
            encrypted_message = rail_fence_cipher_encryption(message, depth)
            print("Message:" ,message)
            print("Depth:" ,depth)
            print ("Encrypted Message",encrypted_message)
                     
        elif action == 'Decrypt':
            decrypted_message = rail_fence_cipher_decryption(message, depth)
            print("Message" ,message)
            print("Depth" ,depth)
            print ("Decrypted Message",decrypted_message)          
    return render_template('indexlab5.html', plain_text=plain_text, depth=depth, encrypted_message=encrypted_message, decrypted_message=decrypted_message)

if __name__ == '__main__':
    app.run(debug=True)

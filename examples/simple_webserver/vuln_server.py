from flask import Flask, request
import time

app = Flask(__name__)

# Define the correct flag
CORRECT_FLAG = "ping{time_attack_test}"


def check_string_vul(str1,str2):
    """
    Check if two strings are equal in a time-attack vulnerable way.
    This function will take longer for equal strings than for different ones.
    """
    if len(str1) != len(str2):
        # time.sleep(0.0000001)
        return False

    for i in range(len(str1)):
        if str1[i] != str2[i]:
            return False
        # Simulate a time delay for each character comparison
        # This is where the timing attack vulnerability lies
    return True



@app.route('/check_flag', methods=['GET'])
def check_flag():
    # Get the flag from the query parameter
    if 'flag' not in request.args:
        return "Flag parameter is missing!", 400
    flag = request.args.get('flag')
    if check_string_vul(flag, CORRECT_FLAG):
        return "Flag is correct!", 200
    else:
        return "Flag is incorrect!", 400

if __name__ == '__main__':
    # Run the server on all interfaces to make it accessible in Docker
    app.run(host='0.0.0.0', port=5000,debug=False)

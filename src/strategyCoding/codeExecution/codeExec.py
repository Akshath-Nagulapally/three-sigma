def exec_with_tests(input_string, error_queue, paper_test = False):

    executioning_code = input_string + "\n" + backtesting

    if paper_test == True:
      executioning_code = input_string + "\n" + backtesting_paper_alpaca_polygon


    print(executioning_code)

    # Create a StringIO object to capture output
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    try:
        # Redirect stdout and stderr to capture logs
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            exec(executioning_code, globals())  # Execute the code globally
    except Exception as e:
        # Capture exception details with only the last few traceback lines
        tb = traceback.format_exc()
        concise_tb = '\n'.join(tb.splitlines()[-5:])  # Keep only the last 5 lines of the traceback
        error_queue.append(f"Exception occurred: {e}\nTraceback:\n{concise_tb}")

    # Capture outputs from stdout and stderr
    stdout_logs = stdout_capture.getvalue()
    stderr_logs = stderr_capture.getvalue()

    # Add captured logs to error_queue or another storage
    error_queue.append(stdout_logs)
    error_queue.append(stderr_logs)

    return stdout_logs, stderr_logs


def paper_trade(input_string, live_override = False):
    """
    Executes the provided code and captures its stdout and stderr logs.

    Parameters:
        executioning_code (str): The code to execute as a string.

    Returns:
        tuple: A tuple containing (stdout_logs, stderr_logs).
    """

    executioning_code = input_string + "\n" + backtesting_paper_alpaca_polygon


    if live_override:
      executioning_code = input_string + "\n" + live_trading_paper



    print(executioning_code)
    exec(executioning_code)

    stdout_stream = io.StringIO()
    stderr_stream = io.StringIO()

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        sys.stdout = stdout_stream
        sys.stderr = stderr_stream

        # Execute the code
        exec(executioning_code)

    except Exception as e:
        # Catch exceptions silently or log as needed
        pass

    finally:
        # Restore stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    # Retrieve the logs
    stdout_logs = stdout_stream.getvalue()
    stderr_logs = stderr_stream.getvalue()

    return stdout_logs, stderr_logs
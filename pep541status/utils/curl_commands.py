from pep541status.utils.shell_utils import execute_get_text


def download_package(urls, output_directory:str):
    print(urls)

    for url in urls:
        # command = f"curl -0 {url} -O"
        command = f"wget {url} -P {output_directory}"
        print(command)
        result = execute_get_text(command)
        print(result)


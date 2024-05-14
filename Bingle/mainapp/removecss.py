import subprocess


def detect_unused_css(html_file, css_file):
    # Command to run PurgeCSS
    command = f"purgecss --css {css_file} --content {html_file} --output {css_file}_purged.css"

    # Run PurgeCSS command using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
        print("Unused CSS removed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)


if __name__ == "__main__":
    html_file = "templates/mainapp/base.html"
    css_file = "static/mainapp/vendor/css/style.css"
    detect_unused_css(html_file, css_file)
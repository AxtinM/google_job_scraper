import logging
from pathlib import Path
from driver_handler import create_driver_handler, set_windows_title
from google_handler import Handler


class FileReader:
    @staticmethod
    def accept_filename():
        # filename = input("\aEnter a valid filename: ")
        # put path to your keywords.txt
        filename = '/home/micky/Downloads/jobber/src/keywords.txt'
        return filename

    @property
    def file_content(self):
        filename = self.accept_filename()
        path_object = Path(filename)
        if path_object.exists():
            print(f"{filename} found...")
            with path_object.open() as file_handler:
                content = [line.strip() for line in file_handler.readlines()]
                if content:
                    return content
                else:
                    print("\aNo keywords in the file specified")
        else:
            print("\aYou might have to check the file name.")


if __name__ == "__main__":
    
    set_windows_title()
    logging.basicConfig(format="## %(message)s", level=logging.INFO)
    driver = create_driver_handler()
    print(driver)
    # these are our helper classes
    google_handler = Handler(driver)


    google_handler.load_google_jobs_page()

    keywords = FileReader().file_content
    if keywords:
        for keyword in keywords:
            print(f"Working on keyword - {keyword}")
            google_handler.keyword_jobsearch(keyword)

    driver.quit()
    input("\aPress Enter to quit...")

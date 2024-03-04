import os
import argparse
import hvac
import fitz

from src.document_querier import (
    DocumentQuerier,
    check_availability,
    download_pdf
)
from src.extract_table import (
    get_detector,
    get_extractor,
    get_page_selector
)

# SIREN
parser = argparse.ArgumentParser(description="Tableaux à trouver")
parser.add_argument(
    "--siren", type=str, default=None, help="Siren recherché"
)
parser.add_argument(
    "--year", type=int, default=None, help="Année de recherche"
)
args = parser.parse_args()
siren = args.siren

# INPI API AUTHENTICATION
client = hvac.Client(
    url="https://vault.lab.sspcloud.fr", token=os.environ["VAULT_TOKEN"]
)
secret = os.environ["VAULT_MOUNT"] + "/" + os.environ["VAULT_TOP_DIR"] + "/inpi-api"
mount_point, secret_path = secret.split("/", 1)
secret_dict = client.secrets.kv.read_secret_version(
    path=secret_path, mount_point=mount_point
)

os.environ['MLFLOW_TRACKING_URI'] = "https://projet-extraction-tableaux-mlflow.user.lab.sspcloud.fr/"
os.environ['MLFLOW_EXPERIMENT_NAME'] = "page_selection"
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://minio.lab.sspcloud.fr'


detector = get_detector()
extractor = get_extractor()
page_selector = get_page_selector()


# RETRIEVING PDF ----------------------

if siren is None:
    siren = "562082909"
if year is None:
    year = 2020

document_querier = DocumentQuerier(secret_dict['data']['data']['USER'], secret_dict['data']['data']['PASSWORD'])
availability, document_id = check_availability(document_querier, siren, year)
PDFbyte = download_pdf(document_querier, document_id)

#token = get_token(
#    secret_dict['data']['data']['USER'], 
#    secret_dict['data']['data']['PASSWORD']
#)
#documents, identifier = get_documents_siren(siren, token)
#download_pdf_bilan(identifier, token, "bilan.pdf")


# DETECTING TABLE ------------------------------

document = fitz.open(stream=PDFbyte, filetype="pdf")
# There can be multiple pages sometimes
page_number = page_selector.get_page_number(document)

document.select([page_number])
# Detection
crops = detector.detect(document)

crops[0].save("cropped_table.png") 






#from ca_extract.extraction.page_selection import DocumentQuerier
#from ca_extract.page_selection.document_querier  import DocumentQuerier
#document_querier = DocumentQuerier(secret_dict['data']['data']['USER'], secret_dict['data']['data']['PASSWORD'])
#availability, document_id = check_availability(document_querier, "562082909", "2020")
#PDFbyte = download_pdf(document_querier, document_id)

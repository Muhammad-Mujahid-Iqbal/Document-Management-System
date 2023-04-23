def test_create_document_metadata(client, test_headers):
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 123,
        "documentPath": "/a/b",
        "documentFileName": "sample.html",
        "mimeType": "application/text"
    }

    response = client.post("/documents/metadata/", headers=test_headers, json=data)

    assert response.status_code == 201


def test_create_document_metadata_fail(client, test_headers):
    data = {
        "customerId": test_headers['customerId'],
        "mimeType": "application/text"
    }

    response = client.post("/documents/metadata/", headers=test_headers, json=data)

    assert response.status_code == 422


def test_create_document_status(client, test_headers):
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 300,
        "documentContentHash": "xdctfvgbhj",
        "documentMetadataHash": "d46ftgyhuji",
        "ingestionStatus": "STARTED",
        "extractionStatus": "STARTED"
    }

    response = client.post("/documents/status/", headers=test_headers, json=data)

    assert response.status_code == 201


def test_create_document_status_fail(client, test_headers):
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 300,
        "documentContentHash": "xdctfvgbhj",
        "documentMetadataHash": "d46ftgyhuji",
        "ingestionStatus": "start",
        "extractionStatus": "start"
    }

    response = client.post("/documents/status/", headers=test_headers, json=data)

    assert response.status_code == 422


def test_summary_failed_extraction_status(client, test_headers):
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 300,
        "documentContentHash": "xdctfvgbhj",
        "documentMetadataHash": "d46ftgyhuji",
        "ingestionStatus": "FAILED",
        "extractionStatus": "FAILED"
    }
    response = client.post("/documents/status/", headers=test_headers, json=data)
    assert response.status_code == 201

    response = client.get("/documents/summary/failed/extraction/{id}".format(id=test_headers['customerId']),
                          headers=test_headers)
    assert response.status_code == 200
    assert response.json().get('Document_Ids') == [300]


def test_summary_failed_ingestion_status(client, test_headers):
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 300,
        "documentContentHash": "xdctfvgbhj",
        "documentMetadataHash": "d46ftgyhuji",
        "ingestionStatus": "FAILED",
        "extractionStatus": "FAILED"
    }
    response = client.post("/documents/status/", headers=test_headers, json=data)
    assert response.status_code == 201

    response = client.get("/documents/summary/failed/ingestion/{id}".format(id=test_headers['customerId']),
                          headers=test_headers)
    assert response.status_code == 200
    assert response.json().get('total_no_of_documents') == 1


def test_summary_mimtype(client, test_headers):
    # create metadata document
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 123,
        "documentPath": "/a/b",
        "documentFileName": "sample.html",
        "mimeType": "application/text"
    }
    response = client.post("/documents/metadata/", headers=test_headers, json=data)
    assert response.status_code == 201

    # create  document status
    data = {
        "customerId": test_headers['customerId'],
        "documentId": 123,
        "documentContentHash": "xdctfvgbhj",
        "documentMetadataHash": "d46ftgyhuji",
        "ingestionStatus": "FAILED",
        "extractionStatus": "FAILED"
    }
    response = client.post("/documents/status/", headers=test_headers, json=data)
    assert response.status_code == 201

    # test summary mimtype url
    response = client.get("/documents/summary/mimetype/{id}".format(id=test_headers['customerId']),
                          headers=test_headers)
    assert response.status_code == 200
    response = response.json()[0]
    assert response['mimetype'] == "application/text"
    assert response['no_of_failed_ingestion_extraction'] == 1
    assert response['no_of_success_ingestion_extraction'] == 0

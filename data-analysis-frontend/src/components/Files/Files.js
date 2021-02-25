import React from 'react';
import Form from 'react-bootstrap/Form';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSync } from '@fortawesome/free-solid-svg-icons';

function Files({ files, getFiles, selectFile }) {
  return (
    <Form className="mt-4 mb-4">
      <Form.Group className="form-group">
        <Form.Label htmlFor="file-select">Choose a file:</Form.Label>
        <FontAwesomeIcon onClick={getFiles} icon={faSync} />
        <Form.Control as="select" size="sm" name="files" id="file-select" onChange={selectFile}>
          <option key="filesSelectDefault" value="">Please select a file</option>
          {files.map(file => <option key={file.id} value={file.id}>{file.name}</option>)}
        </Form.Control>
      </Form.Group>
    </Form>
  );
}

export default Files;
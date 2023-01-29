import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { ErrorProps } from '../interfaces/Interfaces';

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const Error = (props: ErrorProps) => {
    const { children, setError, error, ... other } = props;
    const handleClose = () => setError(false);

    return (
        <div>
        <Modal
            open={error}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2" className="text-justify">
                Error
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }} className="text-justify">
                Uppps, something went wrong.
            </Typography>
            </Box>
        </Modal>
        </div>
    );
}

export default Error;
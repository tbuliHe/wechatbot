const express = require('express');
const multer = require('multer');
const axios = require('axios');
const app = express();
const port = 3000;

const upload = multer();

app.post('/receive', upload.none(), async (req, res) => {
    const formData = req.body;

    console.log('Received message:', formData);

    // 转发消息到Python服务器
    try {
        const response = await axios.post('http://localhost:5000/receive', formData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Response from Python server:', response.data);
        res.status(200).send({ message: 'Message processed successfully', chatgpt_reply: response.data.response });
    } catch (error) {
        console.error('Error forwarding message to Python server:', error);
        res.status(500).send({ error: 'Failed to process message' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

require('dotenv').config();
const express = require('express');
const sql = require('mssql');
const bcrypt = require('bcrypt');
const cors = require('cors');

const app = express();
const port = 3000; // You can choose any port that is free

app.use(cors());
app.use(express.json());

// SQL Connection string directly from the environment variable
const sqlConfig = {
  connectionString: process.env.SQL_CONNECTION_STRING,
  options: {
    encrypt: true, // Necessary for Azure SQL Database
    trustServerCertificate: false // Set to true for local development only
  }
};

app.post('/login', async (req, res) => {
  const { firstName, lastName, password } = req.body;

  try {
    await sql.connect(sqlConfig);
    const result = await sql.query`SELECT PasswordHash FROM Users WHERE FirstName = ${firstName} AND LastName = ${lastName}`;

    if (result.recordset.length > 0) {
      const isValid = await bcrypt.compare(password, result.recordset[0].PasswordHash);
      if (isValid) {
        res.json({ message: "Login successful" });
      } else {
        res.status(401).json({ message: "Authentication failed" });
      }
    } else {
      res.status(404).json({ message: "User not found" });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

const ErrorResponse = require("../utils/errorResponse")

const errorHandler = (err, req, res, next) => {
  let error = { ...err };

  error.message = err.message;

  if (err.message === "CastError") {
    const message = `Resources not found ${err.value}`;
    error = new ErrorResponse(message, 404);
  }

  //Mongoose duplicate
  if (err.code === 11000) {
    const message = "Duplicate filed value entered";
    error = new ErrorResponse(message, 400);
  }

  //Mongoose validation 
  if (err.name === "ValidationError") {
    const message = Object.values(err.errors).map(val => ' '+ val.message);
    error = new ErrorResponse(message, 400);
  }

  res.status(error.codeStatus || 500).json({
    success: false,
    error: error.message || "server error"
  })
} 

module.exports = errorHandler;
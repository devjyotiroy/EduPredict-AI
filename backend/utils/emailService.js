const nodemailer = require("nodemailer");

const transporter = nodemailer.createTransport({
  host: "192.178.211.108",
  port: 587,
  secure: false,
  tls: { servername: "smtp.gmail.com", rejectUnauthorized: false },
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

const sendRegistrationEmail = async (name, email) => {
  await transporter.sendMail({
    from: `"EduPredict AI" <${process.env.EMAIL_USER}>`,
    to: email,
    subject: "Welcome to EduPredict AI – Security Alert",
    html: `
      <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden">
        <div style="background:#4f46e5;padding:24px;text-align:center">
          <h1 style="color:#fff;margin:0;font-size:24px">🎓 EduPredict AI</h1>
        </div>
        <div style="padding:32px">
          <h2 style="color:#1f2937">Hi ${name},</h2>
          <p style="color:#4b5563;font-size:16px;line-height:1.6">
            You have successfully registered on <strong>EduPredict AI</strong>.
          </p>
          <div style="background:#fef3c7;border-left:4px solid #f59e0b;padding:16px;border-radius:4px;margin:24px 0">
            <p style="margin:0;color:#92400e;font-size:14px">
              ⚠️ <strong>Security Alert:</strong> If this registration was not made by you, please change your password immediately.
            </p>
          </div>
          <p style="color:#6b7280;font-size:14px">Stay safe,<br/><strong>EduPredict AI Team</strong></p>
        </div>
      </div>`,
  });
};

const sendPredictionReportEmail = async (name, email, pdfBuffer) => {
  await transporter.sendMail({
    from: `"EduPredict AI" <${process.env.EMAIL_USER}>`,
    to: email,
    subject: "Your EduPredict AI Report",
    html: `
      <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden">
        <div style="background:#4f46e5;padding:24px;text-align:center">
          <h1 style="color:#fff;margin:0;font-size:24px">🎓 EduPredict AI</h1>
        </div>
        <div style="padding:32px">
          <h2 style="color:#1f2937">Hi ${name},</h2>
          <p style="color:#4b5563;font-size:16px;line-height:1.6">
            Your prediction report is ready! Please find the attached PDF for your detailed results.
          </p>
          <div style="background:#ede9fe;border-left:4px solid #4f46e5;padding:16px;border-radius:4px;margin:24px 0">
            <p style="margin:0;color:#3730a3;font-size:14px">
              📊 Your report includes predicted marks, career suggestions, and personalized recommendations.
            </p>
          </div>
          <p style="color:#6b7280;font-size:14px">Best of luck,<br/><strong>EduPredict AI Team</strong></p>
        </div>
      </div>`,
    attachments: [
      {
        filename: "EduPredict_Report.pdf",
        content: pdfBuffer,
        contentType: "application/pdf",
      },
    ],
  });
};

module.exports = { sendRegistrationEmail, sendPredictionReportEmail };

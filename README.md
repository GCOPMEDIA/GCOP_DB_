# GCOP Membership Management System

The GCOP Membership Management System is a Django-based application designed to manage church member information. It provides a comprehensive solution for collecting, storing, and managing member details, family relationships, group affiliations, and more.

## Features

### 1. **Member Registration**

- Collect detailed personal information such as:
  - First Name, Other Names, Date of Birth, Phone Number, and Address.
  - Emergency Contact, Occupation, and Next of Kin details.
  - Place of Residence and Hometown.
- Gender selection with predefined choices (`Male`, `Female`).
- Baptism status and history tracking.

### 2. **Family Information**

- Forms to capture details about family members:
  - **Father**: Name, Phone Number, Membership Status.
  - **Mother**: Name, Phone Number, Membership Status.
  - **Spouse**: Name, Phone Number, Membership Status.
  - **Children**: Name, Phone Number, Membership Status.
  - **Relatives**: Name, Relationship, Phone Number, Membership Status.

### 3. **Church Membership Details**

- Track marital status (`Married`, `Single`, `Divorced`, `Widowed`).
- Record the number of children and close relatives.
- Capture membership details:
  - Date joined the church.
  - Welfare and Tithe card numbers.
  - Church branch selection from predefined options.
  - Group affiliations (e.g., Choir, Ushers, Media, etc.).
  - Position held in the church.

### 4. **Search Functionality**

- Search for members by:
  - First Name, Last Name, or Phone Number.

### 5. **Image Upload**

- Upload member profile images using the `MemberImageUploadForm`.

### 6. **Generate Member Cards and Print PDFs**

- Generate PDF member cards with personal details.
- Downloadable via a dedicated URL.

### 7. **Track Attendance**

- Use QR codes to scan and log attendance.
- Maintain attendance records in the database.

### 8. **Customizable Forms**

- All forms are built using Django's `forms.Form` and `forms.ModelForm` for easy customization and validation.

## Key Forms

### `UserDetailsForm`

Captures personal details such as name, date of birth, phone number, address, and baptism history.

### `FurtherQuestionsForm`

Handles additional details like marital status, number of children, parent status, and church membership details.

### `FatherForm`, `MotherForm`, `SpouseForm`, `SurvivorForm`, `NextForm`

Dedicated forms for capturing family member details.

### `MemberImageUploadForm`

Allows uploading of member profile images.

### `MemberSearchForm`

Provides search functionality for finding members by name or phone number.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo-url.git
   cd GCOP_DB_
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Use the forms to register members, manage family details, and track church-related information.

## Folder Structure

```
GCOP_DB_
├── GCOP_
│   ├── forms.py          # Contains all form definitions
│   ├── models.py         # Database models for members
│   ├── views.py          # Handles application logic
│   ├── urls.py           # URL routing for the app
│   ├── templates/        # HTML templates for the frontend
│   ├── static/           # Static files (CSS, JS, images)
│   └── __init__.py       # App initialization
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the Kobby24 License.

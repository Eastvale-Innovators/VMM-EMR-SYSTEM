const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  const doctor = await prisma.doctor.create({
    data: {
      name: 'Dr.Tiffany',
    },
  });

  const patient = await prisma.patient.create({
    data: {
      name: 'John Doe',
      dob: new Date('1980-01-01'),
    },
  });

  const soapNote = await prisma.soap_Note.create({
    data: {
      doctor_id: doctor.doctor_id,
      patient_id: patient.patient_id,
      date_of_visit: new Date(),
      chief_complaint: 'Headache',
      hpi: 'Severe headache for 3 days',
      past_medical_history: 'Hypertension',
      surgical_history: 'Appendectomy in 2010',
      family_history: 'Father has diabetes',
      social_history: 'Non-smoker, occasional alcohol use',
      allergies: 'Penicillin',
      medications: 'Riboflavin 10mg daily',
      review_of_systems: 'No other complaints',
      height: 170.2,
      weight: 70.5,
      bmi: 24.2,
      blood_pressure: '120/80',
      temperature: 37.0,
      pulse: 72,
      o2_oximeter: 98.5,
      physical_exam: 'Normal physical exam',
      test_results: 'Blood test normal',
      assessment: 'Tension headache',
      plan: 'Prescribed ibuprofen, follow-up in one week',
      follow_up: 'One week later',
    },
  });

  //Easier to incorporate for the backend after when implementing the details on the header
  console.log('Inserted doctor:', doctor);
  console.log('Inserted patient:', patient);
  console.log('Inserted SOAP note:', soapNote);

  const allDoctors = await prisma.doctor.findMany();
  console.log('All doctors:', allDoctors);

}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

// Example Prisma models
type Patient = {
  id: number;
  name: string;
  // ... other fields
};

// Wrapper function example
async function createPatient(patientData: Omit<Patient, 'id'>) {
  try {
    const createdPatient = await prisma.patient.create({
      data: patientData,
    });
    return createdPatient;
  } catch (error) {
    // Handle error
    console.error('Error creating patient:', error);
    throw error; // Or rethrow with custom error
  }
}
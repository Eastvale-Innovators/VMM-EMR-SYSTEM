/*
  Warnings:

  - The primary key for the `Soap_Note` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `allergies` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `assessment` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `assignment_id` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `blood_pressure` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `bmi` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `chief_complaint` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `family_history` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `height` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `hpi` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `medications` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `o2_oximeter` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `past_medical_history` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `physical_exam` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `plan` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `pulse` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `review_of_systems` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `social_history` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `surgical_history` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `temperature` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `test_results` on the `Soap_Note` table. All the data in the column will be lost.
  - You are about to drop the column `weight` on the `Soap_Note` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[subjective_id]` on the table `Soap_Note` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[objective_id]` on the table `Soap_Note` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[assessment_id]` on the table `Soap_Note` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[plan_id]` on the table `Soap_Note` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `assessment_id` to the `Soap_Note` table without a default value. This is not possible if the table is not empty.
  - Added the required column `objective_id` to the `Soap_Note` table without a default value. This is not possible if the table is not empty.
  - Added the required column `plan_id` to the `Soap_Note` table without a default value. This is not possible if the table is not empty.
  - The required column `soap_note_id` was added to the `Soap_Note` table with a prisma-level default value. This is not possible if the table is not empty. Please add this column as optional, then populate it before making it required.
  - Added the required column `subjective_id` to the `Soap_Note` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Soap_Note" DROP CONSTRAINT "Soap_Note_pkey",
DROP COLUMN "allergies",
DROP COLUMN "assessment",
DROP COLUMN "assignment_id",
DROP COLUMN "blood_pressure",
DROP COLUMN "bmi",
DROP COLUMN "chief_complaint",
DROP COLUMN "family_history",
DROP COLUMN "height",
DROP COLUMN "hpi",
DROP COLUMN "medications",
DROP COLUMN "o2_oximeter",
DROP COLUMN "past_medical_history",
DROP COLUMN "physical_exam",
DROP COLUMN "plan",
DROP COLUMN "pulse",
DROP COLUMN "review_of_systems",
DROP COLUMN "social_history",
DROP COLUMN "surgical_history",
DROP COLUMN "temperature",
DROP COLUMN "test_results",
DROP COLUMN "weight",
ADD COLUMN     "assessment_id" TEXT NOT NULL,
ADD COLUMN     "objective_id" TEXT NOT NULL,
ADD COLUMN     "plan_id" TEXT NOT NULL,
ADD COLUMN     "soap_note_id" TEXT NOT NULL,
ADD COLUMN     "subjective_id" TEXT NOT NULL,
ADD CONSTRAINT "Soap_Note_pkey" PRIMARY KEY ("soap_note_id");

-- CreateTable
CREATE TABLE "Subjective" (
    "subjective_id" TEXT NOT NULL,
    "chief_complaint" TEXT,
    "hpi" TEXT,
    "past_medical_history" TEXT,
    "surgical_history" TEXT,
    "family_history" TEXT,
    "social_history" TEXT,
    "allergies" TEXT,
    "medications" TEXT,
    "review_of_systems" TEXT,

    CONSTRAINT "Subjective_pkey" PRIMARY KEY ("subjective_id")
);

-- CreateTable
CREATE TABLE "Objective" (
    "objective_id" TEXT NOT NULL,
    "height" DOUBLE PRECISION,
    "weight" DOUBLE PRECISION,
    "bmi" DOUBLE PRECISION,
    "blood_pressure" TEXT,
    "temperature" DOUBLE PRECISION,
    "pulse" INTEGER,
    "o2_oximeter" DOUBLE PRECISION,
    "physical_exam" TEXT,
    "test_results" TEXT,

    CONSTRAINT "Objective_pkey" PRIMARY KEY ("objective_id")
);

-- CreateTable
CREATE TABLE "Assessment" (
    "assessment_id" TEXT NOT NULL,
    "assessment" TEXT,

    CONSTRAINT "Assessment_pkey" PRIMARY KEY ("assessment_id")
);

-- CreateTable
CREATE TABLE "Plan" (
    "plan_id" TEXT NOT NULL,
    "plan" TEXT,

    CONSTRAINT "Plan_pkey" PRIMARY KEY ("plan_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Soap_Note_subjective_id_key" ON "Soap_Note"("subjective_id");

-- CreateIndex
CREATE UNIQUE INDEX "Soap_Note_objective_id_key" ON "Soap_Note"("objective_id");

-- CreateIndex
CREATE UNIQUE INDEX "Soap_Note_assessment_id_key" ON "Soap_Note"("assessment_id");

-- CreateIndex
CREATE UNIQUE INDEX "Soap_Note_plan_id_key" ON "Soap_Note"("plan_id");

-- AddForeignKey
ALTER TABLE "Soap_Note" ADD CONSTRAINT "Soap_Note_subjective_id_fkey" FOREIGN KEY ("subjective_id") REFERENCES "Subjective"("subjective_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Soap_Note" ADD CONSTRAINT "Soap_Note_objective_id_fkey" FOREIGN KEY ("objective_id") REFERENCES "Objective"("objective_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Soap_Note" ADD CONSTRAINT "Soap_Note_assessment_id_fkey" FOREIGN KEY ("assessment_id") REFERENCES "Assessment"("assessment_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Soap_Note" ADD CONSTRAINT "Soap_Note_plan_id_fkey" FOREIGN KEY ("plan_id") REFERENCES "Plan"("plan_id") ON DELETE RESTRICT ON UPDATE CASCADE;

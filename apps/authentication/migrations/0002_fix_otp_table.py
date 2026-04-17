from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- First, drop any existing constraints
            ALTER TABLE authentication_otpverification DROP CONSTRAINT IF EXISTS authentication_otpverification_phone_number_key;
            
            -- Add email column if it doesn't exist
            ALTER TABLE authentication_otpverification ADD COLUMN IF NOT EXISTS email VARCHAR(254) UNIQUE;
            
            -- Drop phone_number column if it exists
            ALTER TABLE authentication_otpverification DROP COLUMN IF EXISTS phone_number;
            """,
            reverse_sql="""
            -- Reverse: add back phone_number and drop email
            ALTER TABLE authentication_otpverification ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20) UNIQUE;
            ALTER TABLE authentication_otpverification DROP COLUMN IF EXISTS email;
            """
        )
    ]
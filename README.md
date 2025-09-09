# CS2 Tool Login Application

A modern desktop login application for CS2 Tool with Supabase authentication and role-based access control.

## Features

- **Modern UI**: Dark theme with animated buttons and smooth transitions
- **Authentication**: Email/password and OAuth (Google, GitHub) login via Supabase
- **Role-based Access**: FREE and PRO user roles with different dashboard views
- **Session Management**: "Remember me" functionality for persistent login
- **Security**: Secure storage of session tokens using system keyring and encryption

## Requirements

- Python 3.8 or higher
- Microsoft Visual C++ Redistributable for Visual Studio 2019 (required for PyQt6)
- Supabase account and project

## Installation

1. Clone the repository
2. Run the setup script which will check requirements and install dependencies:

```bash
setup_and_run.bat
```

Or manually install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Supabase credentials:

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

## Running the Application

```bash
python main.py
```

If you encounter any issues running the application, especially DLL errors with PyQt6:

1. Run the fix script to automatically resolve common issues:

```bash
RunPyQtFix.bat
```

This script will fix PyQt6 DLL issues without requiring PowerShell execution policy changes.

2. For more detailed solutions, refer to the [Troubleshooting Guide](TROUBLESHOOTING.md).

## Packaging

To create a standalone executable:

```bash
pyinstaller cs2_login.spec
```

The executable will be created in the `dist` directory.

## Supabase Setup

1. Create a Supabase project at https://supabase.com
2. Enable Email/Password and OAuth providers (Google, GitHub) in Authentication settings
3. Create a `profiles` table with the following schema:

```sql
create table profiles (
  id uuid references auth.users on delete cascade not null primary key,
  username text unique not null,
  role text not null default 'FREE',
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create a secure RLS policy
alter table profiles enable row level security;
create policy "Users can view their own profile" on profiles
  for select using (auth.uid() = id);
create policy "Users can update their own profile" on profiles
  for update using (auth.uid() = id);

-- Create a trigger to create a profile when a new user signs up
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, username, role)
  values (new.id, new.email, 'FREE');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
```

## License

MIT
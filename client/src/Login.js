import * as React from 'react';
import {useState} from "react"
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import {Link, useNavigate} from "react-router-dom";
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {useFormik} from 'formik'
import * as Yup from 'yup'
import {MenuBar} from "./Welcome"
import { inMemoryJWTManager } from './inMemoryJWT';

const SignupSchema = Yup.object().shape({  
    id: Yup.number("Must be a number")
        .required("ID Number is required")
        .positive("Should be a positive number")
        .integer("Must be an integer")
  });

const SigninSchema = Yup.object().shape({  
    id: Yup.number("Must be a number")
        .required("ID Number is required")
        .positive("Should be a positive number")
        .integer("Must be an integer"),
  
    password: Yup.string()
      .required("Password is required")
  });

const theme = createTheme();

export function Signin() {
  const navigate = useNavigate();
  let [error, setError] = useState("");
  const formik = useFormik({
    initialValues: {
      id: '',
      password: '',
    },
    validationSchema: SigninSchema,
    onSubmit: (values) => {
        fetch('/api/authenticate?' + new URLSearchParams({
            username: values.id,
            password: values.password
        }))
        .then(res => res.json())
        .then(res => {
            if (res.Token != undefined) {
                inMemoryJWTManager().setToken(res.Token);
                navigate("/dashboard");
            } else {
                setError("Incorrect Credentials!")
            }
        })
      },
  });

  return (
    <ThemeProvider theme={theme}>
      <Container component="main">
        <MenuBar/>
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={formik.handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              value={formik.values.id}
              onChange={formik.handleChange}
              error={formik.touched.id && Boolean(formik.errors.id)}
              helperText={formik.touched.id && formik.errors.id}
              id="id"
              label="Student ID Number"
              name="id"
              autoComplete="Student ID"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              value={formik.values.password}
              onChange={formik.handleChange}
              error={formik.touched.password && Boolean(formik.errors.password)}
              helperText={formik.touched.password && formik.errors.password}
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link to="/forgot">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item xs>
                <p style={{color: "red"}}>
                  {error}
                </p>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export function Signup() {
    let [password, setPassword] = useState("")
    const formik = useFormik({
      initialValues: {
        id: ''
      },
      validationSchema: SignupSchema,
      onSubmit: (values) => {
        fetch('/api/getpassword?' + new URLSearchParams({
            username: values.id,
        }))
        .then(res => res.json())
        .then(res => {
            if (res.Password != undefined) {
                setPassword(`Password: ${res.Password}`);
            }
        })
      },
    });
  
    return (
      <ThemeProvider theme={theme}>
        <Container component="main">
          <MenuBar/>
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Forgot Password
            </Typography>
            <Box component="form" onSubmit={formik.handleSubmit} noValidate sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                value={formik.values.id}
                onChange={formik.handleChange}
                error={formik.touched.id && Boolean(formik.errors.id)}
                helperText={formik.touched.id && formik.errors.id}
                id="id"
                label="Student ID Number"
                name="id"
                autoComplete="Student ID"
                autoFocus
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Forgot Password
              </Button>
              <Grid container>
                <Grid item xs>
                  <p>
                    {password}
                  </p>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </Container>
      </ThemeProvider>
    );
  }


import React, { useState } from 'react'
import FormControl from '@mui/material/FormControl';
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import MuiAlert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const ChangePassword = () => {
    const [values, setValues] = React.useState({
        old_password: '',
        new_password: '',
        confirm_new_password: '',
        showPassword: false,
    });

    const [state, setState] = React.useState({
        open: false,
        vertical: 'top',
        horizontal: 'center',
    });

    const [error, setError] = useState(false)

    const { vertical, horizontal, open } = state;

    const handleChange = (prop) => (event) => {
        setValues({ ...values, [prop]: event.target.value });
    };


    const handleClickShowPassword = () => {
        setValues({
            ...values,
            showPassword: !values.showPassword,
        });
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };


    const handleClick = (newState) => () => {
        if (values.new_password.trim() !== "" && values.confirm_new_password.trim() !== "" && values.new_password === values.confirm_new_password) {
            setError(false)
            setState({ open: true, ...newState });
            const newData = { "old_password": values.old_password, "new_password": values.new_password, "confirm_new_password": values.confirm_new_password }
            console.log(newData);
        }
        else {
            setError(true)
            setValues({ ...values, old_password: '', new_password: '', confirm_new_password: "", showPassword: false })
            setState({ open: true, ...newState });
        }
    };

    const handleClose = () => {
        setState({ ...state, open: false });
    };


    return (
        <div className="enter-forget-pass container-fluid container-fluid d-flex align-items-center justify-content-center">
            <div className="container bg-light">
                <h2>Change Password</h2>
                <FormControl sx={{ width: "100%", marginTop: "1rem" }}>
                    <InputLabel htmlFor="outlined-adornment-password">Old Password</InputLabel>
                    <OutlinedInput

                        sx={{
                            borderRadius: "15px",
                            margin: "0.5rem 0"
                        }}
                        size="small"
                        fullWidth
                        color='success'
                        type={values.showPassword ? 'text' : 'password'}
                        value={values.old_password}
                        onChange={handleChange('old_password')}
                        endAdornment={
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle password visibility"
                                    onClick={handleClickShowPassword}
                                    onMouseDown={handleMouseDownPassword}
                                    edge="end"
                                >
                                    {values.showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                            </InputAdornment>
                        }
                        label="Old Password"
                    />
                </FormControl>
                <FormControl sx={{ width: "100%", margin: "0.5rem 0" }}>
                    <InputLabel htmlFor="outlined-adornment-confirm_password">New Password</InputLabel>
                    <OutlinedInput
                        sx={{
                            borderRadius: "15px",
                            margin: "0.5rem 0"
                        }}
                        size="small"
                        fullWidth
                        color='success'
                        type={values.showPassword ? 'text' : 'password'}
                        value={values.new_password}
                        onChange={handleChange('new_password')}
                        endAdornment={
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle password visibility"
                                    onClick={handleClickShowPassword}
                                    onMouseDown={handleMouseDownPassword}
                                    edge="end"
                                >
                                    {values.showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                            </InputAdornment>
                        }
                        label="New Password"
                    />
                </FormControl>
                <FormControl sx={{ width: "100%", marginBottom: "0.5rem" }}>
                    <InputLabel htmlFor="outlined-adornment-confirm_password">Confirm New Password</InputLabel>
                    <OutlinedInput
                        sx={{
                            borderRadius: "15px",
                            margin: "0.5rem 0"
                        }}
                        size="small"
                        fullWidth
                        color='success'
                        type={values.showPassword ? 'text' : 'password'}
                        value={values.confirm_new_password}
                        onChange={handleChange('confirm_new_password')}
                        endAdornment={
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle password visibility"
                                    onClick={handleClickShowPassword}
                                    onMouseDown={handleMouseDownPassword}
                                    edge="end"
                                >
                                    {values.showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                            </InputAdornment>
                        }
                        label="Confirm New Password"
                    />
                </FormControl>
                <button id='reset-btn' onClick={handleClick({
                    vertical: 'top',
                    horizontal: 'right',
                })}
                >Change Password</button>
            </div>
            <Snackbar open={open} autoHideDuration={3000} onClose={handleClose} anchorOrigin={{ vertical, horizontal }}
                message="I love snacks"
                key={vertical + horizontal}>
                <Alert onClose={handleClose} severity={error === true ? "error" : "success"} sx={{ width: '100%' }}>
                    {error === true ? "Passwords Do Not Match!" : "Password Changed Successfully!"}
                </Alert>
            </Snackbar>
        </div>
    )
}

export default ChangePassword
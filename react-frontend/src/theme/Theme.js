import { createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    type: "light",
    primary: {
      main: "#3aafa9",
      light: "#def2f1",
      medium: "#2B7A78",
      dark: "#17252a",
      contrastText: "#feffff",
    },
    secondary: {
      main: "#2b7a78",
      light: "#3aafa9",
    },
    divider: "#17252a",
    background: {
      default: "#fbfbfb",
    },
  },
  typography: {
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 600,
    fontWeightBold: 700,
  },
});

export default theme;

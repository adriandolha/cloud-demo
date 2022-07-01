import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Item from '@material-ui/core/Grid';
import { Avatar, Box, Link } from '@material-ui/core';
import me from '../static/images/me.jpeg'
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIphoneIcon from '@mui/icons-material/PhoneIphone';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import GitHubIcon from '@mui/icons-material/GitHub';

const useStyles = makeStyles((theme) =>
    createStyles({
        root: {
            flexGrow: 1
        },
        menuButton: {
            marginRight: theme.spacing(2),
        },
        fullName: {
            float: 'left',
            fontFamily: 'sans-serif',
            color: theme.palette.primary.main,
        },
        myTitle: {
            color: theme.palette.success.light,
            float: 'left'
        },
        myPicture: {
            height: 250,
            width: 250,
            borderColor: '#40b281',
            border: '5px solid'
        },
        personalDetails: {
            marginBottom: '20px'
        },
        myDescription: {
            width: 'auto',
            fontFamily: 'Ubuntu !important',
            paddingTop: '10px',
            fontSize: '18px'
        },
        myLink: {
            color: 'black',
            fontSize: '18px',
            // fontFamily: 'Ubuntu !important'
        },
        myIcon: {
            padding: '0 10px 0 10px',
            color: theme.palette.primary.main
        }


    }),
);

function PersonalDetails() {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    return (

        <Grid container spacing={3} columns={{ sm: 3, md: 3, lg: 3 }} className={classes.personalDetails}>
            <Grid item xs={12} md={3} lg={5} container direction='column'>
                <Item>
                    <Typography variant="h4" component="h1" className={classes.fullName}>
                        Adrian Dolha
                    </Typography>
                </Item>
                <Item>
                    <Typography variant="h6" component="h6" className={classes.myTitle} >
                        Senior Software Engineer
                    </Typography>
                </Item>
                <Item>
                    <Typography variant="body1" align='left' className={classes.myDescription}>
                        Accomplished and energetic Senior Architect with a solid history of achievement in Enterprise Software.
                        Motivated leader with strong organizational and prioritization abilities.
                        Seeking to leverage his technical and professional expertise in the latest technologies such as AWS serverless,
                        cloud native microservices and event driven architectures.
                    </Typography>
                </Item>
            </Grid>
            <Grid item lg={2}>
                <Item>
                    <Box display="flex" justifyContent="center">
                        <Avatar alt="" src={me} className={classes.myPicture} />
                    </Box>
                </Item>
            </Grid>
            <Grid item xs={12} md={5} lg={5} container direction='column' spacing={1}>
                <Grid item container direction='row' justifyContent='flex-end' alignItems='center' columns={{ sm: 1, md: 2, lg: 2 }}>
                    <Typography variant='h6'>adrian.dolha1@gmail.com</Typography>
                    <EmailIcon className={classes.myIcon} />
                </Grid>
                <Grid item container direction='row' justifyContent='flex-end' alignItems='center' columns={{ sm: 1, md: 2, lg: 2 }}>
                    <Typography variant='h6'>+40743389452</Typography>
                    <PhoneIphoneIcon className={classes.myIcon} />
                </Grid>
                <Grid item container direction='row' justifyContent='flex-end' alignItems='center' columns={{ sm: 1, md: 2, lg: 2 }}>
                    <Typography variant='h6'>Cluj-Napoca, Romania</Typography>
                    <LocationOnIcon className={classes.myIcon} />
                </Grid>
                <Grid item container direction='row' justifyContent='flex-end' alignItems='center'>
                    <Link href="https://www.linkedin.com/in/adrian-dolha-562578b8/" className={classes.myLink}>
                        <Typography variant='h6'>linkedin.com/in/adrian-dolha-562578b8</Typography>
                    </Link>
                    <LinkedInIcon className={classes.myIcon} />
                </Grid>
                <Grid item container direction='row' justifyContent='flex-end' alignItems='center'>
                    <Link href="https://github.com/adriandolha" className={classes.myLink}>
                        <Typography variant='h6'>github.com/in/adriandolha</Typography>
                    </Link>
                    <GitHubIcon className={classes.myIcon} />
                </Grid>
            </Grid>
        </Grid>

    );
}

export default PersonalDetails;

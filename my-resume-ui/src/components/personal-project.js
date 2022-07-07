import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { List, ListItem, Link } from '@material-ui/core';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import CircleIcon from '@mui/icons-material/Circle';
import { Fragment, useEffect } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';

const useStyles = makeStyles((theme) =>
    createStyles({
        projectTitle: {
            float: 'left',
            fontWeight: 'bold'
        },
        myLink: {
            color: 'black',
            fontSize: '18px',
            // fontFamily: 'Ubuntu !important'
        },
        myIcon: {
            padding: '0 10px 0 0',
            color: theme.palette.primary.main
        },
        personalProject: {
            marginRight: theme.spacing(2)
        },
        work: {
            marginTop: '10px'
        },
        workDate: {
            fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        },
        tasks: {
            fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        },
        taskList: {
            listStyleType: 'circle',
            marginBottom: theme.spacing(1)
        },
        taskListItem: {
            padding: '0'
        },
        techStack: {
            borderRadius: '10px',
            backgroundColor: theme.palette.primary.main,
            float: 'left',
            padding: '1px 10px 1px 10px',
            margin: '3px 3px 3px 3px',
            color: 'white'
        }
    }),
);

function PersonalProject({ resume, data }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);

    return (
        <Grid item container xs={12} md={12} lg={12} direction='column' >
            <Grid item container direction='column' >
                <Grid item>
                    <Typography variant="h6" className={classes.projectTitle}>
                        {`${data.title} (${data.from} - ${data.to})`}
                    </Typography>
                </Grid>
                <Grid item container direction='row' justifyContent='flex-start' alignItems='center'>
                    <GitHubIcon className={classes.myIcon} />
                    <Link href={data.github.link} className={classes.myLink}>
                        <Typography variant='body1'>{data.github.placeholder}</Typography>
                    </Link>
                </Grid>

            </Grid>

            <Grid item>
                <List className={classes.taskList} dense={true} disablePadding={true}>
                    {data.tasks && data.tasks.map((task, i) => (
                        <Fragment key={i}>
                            <ListItem className={classes.taskListItem} >
                                <CircleIcon sx={{ padding: '0 10px 0 0', margin: '0', fontSize: '8px', color: theme.palette.success.dark }} />
                                <Typography variant='body1'>{task}</Typography>
                            </ListItem>
                        </Fragment>
                    ))}
                </List>
                {data.techStack && data.techStack.map(techStack => (
                    <Fragment key={techStack}><Typography variant='body1' className={classes.techStack}>{techStack}</Typography></Fragment>
                ))}

            </Grid>
        </Grid>
    );
}

export default PersonalProject;
